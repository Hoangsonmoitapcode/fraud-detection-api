"""
Script to populate phone headings database with international data
"""
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import PhoneHeading

# International phone country codes and regions
INTERNATIONAL_HEADINGS = [
    # Vietnam (Safe)
    {"+84": "Vietnam"},
    
    # Traditional Vietnam carriers
    {"096": "Vietnam"}, {"097": "Vietnam"}, {"098": "Vietnam"},
    {"032": "Vietnam"}, {"033": "Vietnam"}, {"034": "Vietnam"},
    {"035": "Vietnam"}, {"036": "Vietnam"}, {"037": "Vietnam"},
    {"038": "Vietnam"}, {"039": "Vietnam"}, {"070": "Vietnam"},
    {"076": "Vietnam"}, {"077": "Vietnam"}, {"078": "Vietnam"},
    {"079": "Vietnam"}, {"081": "Vietnam"}, {"082": "Vietnam"},
    {"083": "Vietnam"}, {"084": "Vietnam"}, {"085": "Vietnam"},
    {"088": "Vietnam"}, {"091": "Vietnam"}, {"094": "Vietnam"},
    
    # iTel (Indochina Telecom) - New carrier
    {"087": "Vietnam"},  # iTel main prefix
    
    # Vietnamobile (VTC Mobile)
    {"092": "Vietnam"}, {"056": "Vietnam"}, {"058": "Vietnam"},
    
    # Wintel (VNPT subsidiary)
    {"099": "Vietnam"},  # Wintel main prefix
    
    # VNPAY Sky (Digital wallet carrier)
    {"089": "Vietnam"},  # VNPAY Sky main prefix
    
    # Additional Vietnam prefixes (recent allocations)
    {"059": "Vietnam"}, {"090": "Vietnam"}, {"093": "Vietnam"}, {"095": "Vietnam"},
    
    # International (Potentially Unsafe)
    {"+1": "USA/Canada"}, {"+44": "United Kingdom"}, {"+86": "China"},
    {"+91": "India"}, {"+81": "Japan"}, {"+49": "Germany"},
    {"+33": "France"}, {"+39": "Italy"}, {"+34": "Spain"},
    {"+7": "Russia"}, {"+55": "Brazil"}, {"+52": "Mexico"},
    {"+61": "Australia"}, {"+27": "South Africa"}, {"+20": "Egypt"},
    {"+234": "Nigeria"}, {"+254": "Kenya"}, {"+66": "Thailand"},
    {"+65": "Singapore"}, {"+60": "Malaysia"}, {"+62": "Indonesia"},
    {"+63": "Philippines"}, {"+82": "South Korea"}, {"+90": "Turkey"},
    {"+98": "Iran"}, {"+92": "Pakistan"}, {"+880": "Bangladesh"},
    {"+94": "Sri Lanka"}, {"+95": "Myanmar"}, {"+856": "Laos"},
    {"+855": "Cambodia"}, {"+673": "Brunei"}, {"+976": "Mongolia"},
    
    # Common scam/fraud origins (marked as unsafe)
    {"+380": "Ukraine"}, {"+375": "Belarus"}, {"+373": "Moldova"},
    {"+996": "Kyrgyzstan"}, {"+998": "Uzbekistan"}, {"+992": "Tajikistan"},
    {"+993": "Turkmenistan"}, {"+994": "Azerbaijan"}, {"+995": "Georgia"},
    {"+374": "Armenia"}, {"+371": "Latvia"}, {"+372": "Estonia"},
    {"+370": "Lithuania"}, {"+48": "Poland"}, {"+420": "Czech Republic"},
    {"+421": "Slovakia"}, {"+36": "Hungary"}, {"+40": "Romania"},
    {"+359": "Bulgaria"}, {"+385": "Croatia"}, {"+381": "Serbia"},
    {"+382": "Montenegro"}, {"+383": "Kosovo"}, {"+389": "North Macedonia"},
    {"+386": "Slovenia"}, {"+387": "Bosnia and Herzegovina"}
]

def populate_phone_headings():
    """Populate the phone_headings table with international data"""
    db: Session = SessionLocal()
    
    try:
        # Don't clear existing data - just add new ones
        # db.query(PhoneHeading).delete()
        # db.commit()
        
        headings_added = 0
        
        for heading_dict in INTERNATIONAL_HEADINGS:
            for heading, region in heading_dict.items():
                # Vietnam numbers are safe, others are potentially unsafe
                status = "safe" if region == "Vietnam" else "unsafe"
                
                # Check if heading already exists
                existing = db.query(PhoneHeading).filter(
                    PhoneHeading.heading == heading
                ).first()
                
                if not existing:
                    phone_heading = PhoneHeading(
                        heading=heading,
                        region=region,
                        status=status
                    )
                    db.add(phone_heading)
                    headings_added += 1
        
        db.commit()
        print(f"✅ Successfully added {headings_added} phone headings to database")
        
        # Show summary
        safe_count = db.query(PhoneHeading).filter(PhoneHeading.status == "safe").count()
        unsafe_count = db.query(PhoneHeading).filter(PhoneHeading.status == "unsafe").count()
        
        print(f"📊 Summary:")
        print(f"   - Safe headings: {safe_count}")
        print(f"   - Unsafe headings: {unsafe_count}")
        print(f"   - Total headings: {safe_count + unsafe_count}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error populating headings: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    populate_phone_headings()
