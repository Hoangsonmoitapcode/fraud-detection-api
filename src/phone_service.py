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
        # Mobile numbers are considered safe
        vietnam_mobile_safe = [
            '096', '097', '098', '032', '033', '034', '035', '036', '037', '038', '039',
            '070', '076', '077', '078', '079', '081', '082', '083', '084', '085', '088',
            '091', '094', '087', '092', '056', '058', '099', '089', '059', '090', '093', '095'
        ]
        
        # Landline numbers are considered unsafe due to spoofing risks
        vietnam_landline_unsafe = {
            '024': 'Hà Nội',           # Hanoi
            '028': 'TP.HCM',          # Ho Chi Minh City
            '025': 'Hải Phòng',       # Hai Phong
            '026': 'Đà Nẵng',         # Da Nang
            '027': 'Cần Thơ',         # Can Tho
            '029': 'Nghệ An',         # Nghe An
            '020': 'Thái Bình',       # Thai Binh
            '021': 'Hải Dương',       # Hai Duong
            '022': 'Nam Định',        # Nam Dinh
            '023': 'Ninh Bình',       # Ninh Binh
            '0203': 'Hà Giang',       # Ha Giang
            '0204': 'Cao Bằng',       # Cao Bang
            '0206': 'Lạng Sơn',       # Lang Son
            '0208': 'Tuyên Quang',    # Tuyen Quang
            '0209': 'Lào Cai',        # Lao Cai
            '0210': 'Điện Biên',      # Dien Bien
            '0211': 'Lai Châu',       # Lai Chau
            '0212': 'Sơn La',         # Son La
            '0213': 'Yên Bái',        # Yen Bai
            '0214': 'Hoà Bình',       # Hoa Binh
            '0215': 'Thái Nguyên',    # Thai Nguyen
            '0216': 'Lạng Sơn',       # Lang Son (alternative)
            '0218': 'Phú Thọ',        # Phu Tho
            '0219': 'Vĩnh Phúc',      # Vinh Phuc
            '0220': 'Bắc Giang',      # Bac Giang
            '0221': 'Bắc Kạn',        # Bac Kan
            '0222': 'Quảng Ninh',     # Quang Ninh
            '0225': 'Hải Dương',      # Hai Duong
            '0226': 'Hưng Yên',       # Hung Yen
            '0227': 'Hà Nam',         # Ha Nam
            '0228': 'Thái Bình',      # Thai Binh
            '0229': 'Nam Định',       # Nam Dinh
            '0230': 'Ninh Bình',      # Ninh Binh
            '0231': 'Thanh Hóa',      # Thanh Hoa
            '0232': 'Nghệ An',        # Nghe An
            '0233': 'Hà Tĩnh',        # Ha Tinh
            '0234': 'Quảng Bình',     # Quang Binh
            '0235': 'Quảng Trị',      # Quang Tri
            '0236': 'Thừa Thiên Huế', # Thua Thien Hue
            '0237': 'Quảng Nam',      # Quang Nam
            '0238': 'Kon Tum',        # Kon Tum
            '0239': 'Quảng Ngãi',     # Quang Ngai
            '0240': 'Gia Lai',        # Gia Lai
            '0241': 'Bình Định',      # Binh Dinh
            '0242': 'Phú Yên',        # Phu Yen
            '0243': 'Đắk Lắk',        # Dak Lak
            '0244': 'Khánh Hòa',      # Khanh Hoa
            '0245': 'Lâm Đồng',       # Lam Dong
            '0246': 'Ninh Thuận',     # Ninh Thuan
            '0247': 'Tây Ninh',       # Tay Ninh
            '0248': 'Bình Phước',     # Binh Phuoc
            '0249': 'Đắk Nông',       # Dak Nong
            '0250': 'Bình Thuận',     # Binh Thuan
            '0251': 'Bà Rịa-Vũng Tàu', # Ba Ria-Vung Tau
            '0252': 'Đồng Nai',       # Dong Nai
            '0253': 'Bình Dương',     # Binh Duong
            '0254': 'Long An',        # Long An
            '0255': 'Tiền Giang',     # Tien Giang
            '0256': 'Bến Tre',        # Ben Tre
            '0257': 'Vĩnh Long',      # Vinh Long
            '0258': 'Trà Vinh',       # Tra Vinh
            '0259': 'An Giang',       # An Giang
            '0260': 'Đồng Tháp',      # Dong Thap
            '0261': 'Kiên Giang',     # Kien Giang
            '0262': 'Cà Mau',         # Ca Mau
            '0263': 'Hậu Giang',      # Hau Giang
            '0269': 'Bạc Liêu',       # Bac Lieu
            '0270': 'Sóc Trăng',      # Soc Trang
            '0271': 'Cần Thơ',        # Can Tho (alternative)
            '0272': 'An Giang',       # An Giang (alternative)
            '0273': 'Kiên Giang',     # Kien Giang (alternative)
            '0274': 'Cà Mau',         # Ca Mau (alternative)
            '0275': 'Bạc Liêu',       # Bac Lieu (alternative)
            '0276': 'Sóc Trăng',      # Soc Trang (alternative)
            '0277': 'An Giang',       # An Giang (alternative)
            '0278': 'Vĩnh Long',      # Vinh Long (alternative)
            '0279': 'Cần Thơ'         # Can Tho (alternative)
        }
        
        if phone_head in vietnam_mobile_safe or phone_head == '+84':
            return "Vietnam", "safe", None
        elif phone_head in vietnam_landline_unsafe:
            region = f"Vietnam - {vietnam_landline_unsafe[phone_head]}"
            return region, "unsafe", None
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
