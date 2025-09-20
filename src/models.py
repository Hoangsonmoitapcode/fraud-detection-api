
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class PhoneHeading(Base):
    __tablename__ = "phone_headings"
    id = Column(Integer, primary_key=True, index=True)
    heading = Column(String, nullable=False, unique=True)  # e.g., "096", "+84", "+1"
    region = Column(String, nullable=False)  # e.g., "Vietnam", "USA"
    status = Column(String, nullable=False)  # "safe" or "unsafe"
    
    # Relationship to users
    users = relationship("User", back_populates="heading_info")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String, nullable=False)
    phone_head = Column(String, nullable=False)
    phone_region = Column(String, nullable=False)
    label = Column(String, nullable=True)
    heading_id = Column(Integer, ForeignKey("phone_headings.id"), nullable=True)
    
    # Relationship to phone heading
    heading_info = relationship("PhoneHeading", back_populates="users")


class SmsScam(Base):
    __tablename__ = "sms_scams"
    id = Column(Integer, primary_key=True, index=True)
    sms_content = Column(String, nullable=False)  # Nội dung SMS scam
    label = Column(String, nullable=False)  # "spam" or "safe"


class BankingScam(Base):
    __tablename__ = "banking_scams"
    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String, nullable=False)  # Số tài khoản scam
    bank_name = Column(String, nullable=False)  # Tên ngân hàng thụ hưởng


class WebsiteScam(Base):
    __tablename__ = "website_scams"
    id = Column(Integer, primary_key=True, index=True)
    website_url = Column(String, nullable=False)  # URL website scam
    label = Column(String, nullable=False)  # "scam" or "safe"


