from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

class PhoneHeadingCreate(BaseModel):
    heading: str = Field(
        ..., 
        title="Phone Heading", 
        description="Phone number prefix (e.g., '096', '+84', '+1')",
        example="096"
    )
    region: str = Field(
        ..., 
        title="Region", 
        description="Country or region name",
        example="Vietnam"
    )
    status: str = Field(
        ..., 
        title="Status", 
        description="Safety status: 'safe' or 'unsafe'",
        example="safe"
    )

class PhoneHeadingResponse(BaseModel):
    id: int = Field(..., title="ID", description="Unique identifier")
    heading: str = Field(..., title="Phone Heading")
    region: str = Field(..., title="Region")
    status: str = Field(..., title="Status")
    
    class Config:
        from_attributes = True

class PhoneNumberCreate(BaseModel):
    phone_numbers: List[str] = Field(
        ...,
        title="Phone Numbers List",
        description="List of phone numbers to create records for (1 or more)",
        example=["0965842855", "0123456789", "+84987654321"],
        min_items=1,
        max_items=50  # Limit for database operations
    )


class BatchPhoneAnalyze(BaseModel):
    phone_numbers: List[str] = Field(
        ...,
        title="Phone Numbers List",
        description="List of phone numbers to analyze (no database save)",
        example=["0965842855", "0123456789", "+84987654321"],
        min_items=1,
        max_items=100  # Higher limit since no database writes
    )

class ConfirmRiskyRequest(BaseModel):
    phone_number: str = Field(
        ..., 
        title="Phone Number", 
        description="Phone number to confirm as risky",
        example="0965842855"
    )
    confirmation_type: str = Field(
        ..., 
        title="Confirmation Type", 
        description="Type of confirmation: 'risky', 'scam', or 'spam'",
        example="scam"
    )

class PhoneNumberResponse(BaseModel):
    id: int = Field(..., title="Phone Number ID", description="Unique identifier")
    phone_number: str = Field(..., title="Phone Number")
    phone_head: str = Field(..., title="Phone Head", description="Auto-detected phone prefix")
    phone_region: str = Field(..., title="Phone Region", description="Auto-detected region")
    label: Optional[str] = Field(None, title="Label", description="Auto-detected safety status")
    heading_id: Optional[int] = Field(None, title="Heading ID", description="Reference to phone heading")
    
    class Config:
        from_attributes = True


# SMS Scam Schemas
class SmsScamItem(BaseModel):
    sms_content: str = Field(
        ..., 
        title="SMS Content", 
        description="Nội dung tin nhắn SMS để phân tích",
        example="Chúc mừng! Bạn đã trúng thưởng 100 triệu. Truy cập link: http://scam-site.com"
    )
    label: str = Field(
        ..., 
        title="Label", 
        description="Phân loại: 'spam' hoặc 'safe'",
        example="spam"
    )


class SmsScamCreate(BaseModel):
    sms_messages: List[SmsScamItem] = Field(
        ...,
        title="SMS Messages List", 
        description="List of SMS messages to report as spam/safe (1 or more)",
        example=[
            {"sms_content": "Chúc mừng! Bạn trúng thưởng 100 triệu", "label": "spam"},
            {"sms_content": "Cuộc họp lúc 2pm hôm nay", "label": "safe"}
        ],
        min_items=1,
        max_items=50
    )


class SmsScamResponse(BaseModel):
    id: int = Field(..., title="SMS ID", description="Unique identifier")
    sms_content: str = Field(..., title="SMS Content")
    label: str = Field(..., title="Label")
    
    class Config:
        from_attributes = True


# Banking Scam Schemas
class BankingScamItem(BaseModel):
    account_number: str = Field(
        ..., 
        title="Account Number", 
        description="Số tài khoản ngân hàng được báo cáo lừa đảo",
        example="1234567890"
    )
    bank_name: str = Field(
        ..., 
        title="Bank Name", 
        description="Tên ngân hàng thụ hưởng",
        example="Vietcombank"
    )


class BankingScamCreate(BaseModel):
    banking_accounts: List[BankingScamItem] = Field(
        ...,
        title="Banking Accounts List",
        description="List of banking accounts to report as scam (1 or more)",
        example=[
            {"account_number": "1234567890", "bank_name": "Vietcombank"},
            {"account_number": "0987654321", "bank_name": "Techcombank"}
        ],
        min_items=1,
        max_items=50
    )


class BankingScamResponse(BaseModel):
    id: int = Field(..., title="Banking ID", description="Unique identifier")
    account_number: str = Field(..., title="Account Number")
    bank_name: str = Field(..., title="Bank Name")
    
    class Config:
        from_attributes = True


# Website Scam Schemas
class WebsiteScamItem(BaseModel):
    website_url: str = Field(
        ..., 
        title="Website URL", 
        description="URL của website lừa đảo",
        example="https://fake-bank-site.com"
    )
    label: str = Field(
        ..., 
        title="Label", 
        description="Phân loại: 'scam' hoặc 'safe'",
        example="scam"
    )


class WebsiteScamCreate(BaseModel):
    websites: List[WebsiteScamItem] = Field(
        ...,
        title="Websites List",
        description="List of websites to report as scam/safe (1 or more)",
        example=[
            {"website_url": "https://fake-bank-site.com", "label": "scam"},
            {"website_url": "https://phishing-site.org", "label": "scam"}
        ],
        min_items=1,
        max_items=50
    )


class WebsiteScamResponse(BaseModel):
    id: int = Field(..., title="Website ID", description="Unique identifier")
    website_url: str = Field(..., title="Website URL")
    label: str = Field(..., title="Label")
    
    class Config:
        from_attributes = True
