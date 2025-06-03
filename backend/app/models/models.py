#models.py
"""
SQLAlchemy models for the database tables.
Defines the structure of the 'users', 'license', and 'license_codes' tables.
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base 
from datetime import datetime

class User(Base):
    """
    Represents a user in the 'users' table.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String) # Hashed password
    is_active = Column(Boolean, default=False) # Indicates if the user account is active
    expiration_date = Column(DateTime, nullable=True) # Account expiration date
    
    # Relationship with LicenseCode
    license_code = relationship("LicenseCode", back_populates="user", uselist=False)

class License(Base):
    """
    Represents a generic license type in the 'license' table.
    Note: This model name might be slightly confusing given the 'license_codes' table.
    It seems to store properties of a license type (like duration), not individual codes.
    Consider renaming this model or clarifying its purpose if needed.
    """
    __tablename__ = "license"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, nullable=False) # Unique identifier for the license type?
    is_used = Column(Integer, default=0) 
    duration_days = Column(Integer, nullable=False)  
    
class LicenseCode(Base):
    """
    Represents a specific generated license code in the 'license_codes' table.
    These are the individual codes users will activate.
    """
    __tablename__ = "license_codes"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    is_used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    used_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationship with User
    user = relationship("User", back_populates="license_code")

    def __repr__(self):
        return f"<LicenseCode {self.code}>"     