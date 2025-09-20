"""
Phone number parsing and fraud detection service
"""
import re
from typing import Optional, Tuple
from sqlalchemy.orm import Session
from .models import PhoneHeading

class PhoneService:
    @staticmethod
    def extract_phone_head(phone_number: str) -> str:
        """
        Extract phone heading from phone number
        Handles both international (+84...) and domestic (096...) formats
        """
        # Remove spaces and special characters except +
        cleaned = re.sub(r'[^\d+]', '', phone_number)
        
        # International format (+84, +1, etc.)
        if cleaned.startswith('+'):
            # Common country code patterns
            # Single digit: +1, +7
            if re.match(r'^\+[17]', cleaned):
                return cleaned[:2]
            # Two digits: +44, +49, +33, +39, +34, +81, +82, +86, +91, +98, +92, +94, +95, +90, +66, +65, +60, +62, +63
            elif re.match(r'^\+(?:44|49|33|39|34|81|82|86|91|98|92|94|95|90|66|65|60|62|63|84|20|27|55|52|61)', cleaned):
                return cleaned[:3]
            # Three digits: +234, +254, +880, +856, +855, +673, +976, +380, +375, +373, +996, +998, +992, +993, +994, +995, +374, +371, +372, +370, +420, +421, +385, +381, +382, +383, +389, +386, +387
            elif re.match(r'^\+(?:234|254|880|856|855|673|976|380|375|373|996|998|992|993|994|995|374|371|372|370|420|421|385|381|382|383|389|386|387)', cleaned):
                return cleaned[:4]
            # Default: extract up to 4 digits after +
            else:
                match = re.match(r'(\+\d{1,4})', cleaned)
                if match:
                    return match.group(1)
        
        # Domestic format - extract first 3-4 digits
        if len(cleaned) >= 3:
            # For Vietnamese numbers, typically 3 digits (096, 097, etc.)
            if cleaned.startswith('0') and len(cleaned) >= 3:
                return cleaned[:3]
            # For other formats, try first 3-4 digits
            elif len(cleaned) >= 4:
                return cleaned[:4]
            else:
                return cleaned[:3]
        
        return cleaned

    @staticmethod
    def detect_region_and_status(phone_head: str, db: Session) -> Tuple[str, str, Optional[int]]:
        """
        Detect region and safety status based on phone heading
        Returns: (region, status, heading_id)
        """
        # Query database for phone heading
        heading_info = db.query(PhoneHeading).filter(
            PhoneHeading.heading == phone_head
        ).first()
        
        if heading_info:
            return heading_info.region, heading_info.status, heading_info.id
        
        # Default logic if not found in database
        # Vietnam headings are considered safe
        vietnam_headings = ['096', '097', '098', '032', '033', '034', '035', '036', '037', '038', '039']
        
        if phone_head in vietnam_headings or phone_head == '+84':
            return "Vietnam", "safe", None
        else:
            # Unknown headings are considered unsafe (potential fraud)
            return "Unknown", "unsafe", None

    @staticmethod
    def analyze_phone_number(phone_number: str, db: Session) -> dict:
        """
        Complete phone number analysis
        Returns dictionary with all extracted information
        """
        phone_head = PhoneService.extract_phone_head(phone_number)
        region, status, heading_id = PhoneService.detect_region_and_status(phone_head, db)
        
        return {
            "phone_head": phone_head,
            "phone_region": region,
            "label": status,
            "heading_id": heading_id
        }
