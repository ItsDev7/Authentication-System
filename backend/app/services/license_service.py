"""
Service layer for handling license code business logic.
Includes functions for generating, creating, validating, and activating license codes.
"""

import secrets
import string
from datetime import datetime, timedelta, UTC
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# Local models
from app.models.models import LicenseCode
from app.models.models import User

class LicenseService:
    """
    Provides static methods for license code operations.
    """

    @staticmethod
    def generate_code(length: int = 16) -> str:
        """Generate a random alphanumeric license code of a specified length."""
        # Define the characters to use for the code
        alphabet = string.ascii_uppercase + string.digits
        # Generate the code by randomly selecting characters
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    @staticmethod
    async def create_license_code(db: AsyncSession, duration_days: int = 30) -> LicenseCode:
        """Create a new license code with a given duration."""
        try:
            # Generate a unique code
            code = LicenseService.generate_code()
            
            # Get current time in UTC and convert to naive datetime
            current_time = datetime.now(UTC).replace(tzinfo=None)
            
            # Calculate expiration time (also naive)
            expires_at = current_time + timedelta(days=duration_days)

            # Create a new LicenseCode instance with naive timestamps
            license_code = LicenseCode(
                code=code,
                is_used=False,
                created_at=current_time,
                expires_at=expires_at,
                used_by=None
            )

            # Add the new code to the database session
            db.add(license_code)
            
            # Commit the transaction
            await db.commit()
            
            # Refresh the instance to load database-generated attributes
            await db.refresh(license_code)
            
            return license_code
            
        except Exception as e:
            # Rollback the transaction in case of error
            await db.rollback()
            raise Exception(f"Failed to create license code: {str(e)}")

    @staticmethod
    async def validate_code(db: AsyncSession, code: str) -> tuple[bool, str, str | None]:
        """Validate a license code by checking its existence, usage status, and expiration."""
        try:
            # Query the database for the license code
            result = await db.execute(select(LicenseCode).filter(LicenseCode.code == code))
            license_code = result.scalars().first()

            # Check if the code exists
            if not license_code:
                return False, "Invalid license code", None
                
            # Check if the code has already been used
            if license_code.is_used:
                return False, "License code already used", None
                
            # Check if the code has expired
            current_time = datetime.now(UTC).replace(tzinfo=None)
            if license_code.expires_at < current_time:
                return False, "License code has expired", None

            # If all checks pass, the code is valid
            return True, "License code is valid", license_code.expires_at.isoformat() if license_code.expires_at else None
            
        except Exception as e:
            raise Exception(f"Failed to validate license code: {str(e)}")

    @staticmethod
    async def activate_code(db: AsyncSession, code: str, user_id: int) -> tuple[bool, str, str | None]:
        """Activate a license code for a specific user."""
        try:
            # Validate the code first
            is_valid, message, expires_at = await LicenseService.validate_code(db, code)
            if not is_valid:
                return False, message, None

            # Retrieve the license code and user
            result = await db.execute(select(LicenseCode).filter(LicenseCode.code == code))
            license_code = result.scalars().first()
            user = await db.get(User, user_id)

            if not license_code or not user:
                return False, "Internal error: License code or user not found after validation.", None

            # Mark the license code as used and link it to the user
            license_code.is_used = True
            license_code.used_by = user_id

            # Update the user's account status and expiration date
            user.is_active = True
            user.expiration_date = license_code.expires_at

            # Add updated objects to the session
            db.add(license_code)
            db.add(user)
            
            # Commit the changes
            await db.commit()

            return True, "License activated successfully", license_code.expires_at.isoformat() if license_code.expires_at else None
            
        except Exception as e:
            # Rollback the transaction in case of error
            await db.rollback()
            raise Exception(f"Failed to activate license code: {str(e)}") 