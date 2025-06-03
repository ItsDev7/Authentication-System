# schema.py
"""
Pydantic schemas for various data structures used in the application.
Includes schemas for user creation, license verification, and license codes.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    """
    Schema for user creation (used in signup and login).
    """
    username: str # The username for the user
    password: str # The password for the user

    
class LicenseVerify(BaseModel):
    """
    Schema for verifying a license key.
    Used when a user submits a license key for activation.
    """
    username: str # The username of the user attempting to verify the license
    key: str # The license key provided by the user
    
class LicenseCodeBase(BaseModel):
    """
    Base schema for license codes.
    Contains common fields for license codes.
    """
    code: str # The unique license code string
    expires_at: datetime # Expiration date of the license code


class LicenseCodeResponse(LicenseCodeBase):
    """
    Schema for responding with license code details.
    Includes database-generated fields for display.
    """
    id: int # Unique identifier of the license code in the database
    is_used: bool # Whether the license code has been used
    created_at: datetime # Timestamp when the license code was created
    used_by: Optional[int] = None # ID of the user who used the code (if any)

    class Config:
        """
        Pydantic configuration for the model.
        Enables ORM mode to automatically convert SQLAlchemy models to this schema.
        """
        from_attributes = True # Allow mapping from ORM objects     