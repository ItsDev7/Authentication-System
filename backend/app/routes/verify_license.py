"""
Router for verifying and activating user licenses.
Provides an endpoint to activate a user account using a valid license key.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..schemas.schema import LicenseVerify
from ..models.models import License, User
from datetime import datetime, timedelta, UTC
from ..core.database import get_db
import traceback

router = APIRouter()

@router.post("/verify_license/")
async def verify_license(
    data: LicenseVerify,
    db: AsyncSession = Depends(get_db)
):
    """
    Verifies a license key and activates the associated user account.
    Sets the user's account as active and calculates the expiration date.
    """
    try:
        result = await db.execute(select(License).where(License.key == data.key))
        license_entry = result.scalars().first()

        if not license_entry:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="License key is invalid")

        if license_entry.is_used == 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="License key has already been used")

        user_result = await db.execute(select(User).where(User.username == data.username))
        user = user_result.scalars().first()

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        user.is_active = True
        user.expiration_date = datetime.now(UTC) + timedelta(days=license_entry.duration_days)

        license_entry.is_used = 1

        db.add(user)
        db.add(license_entry)
        await db.commit()

        return {"message": "Account activated successfully", "expires_at": user.expiration_date.isoformat()}

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        error_details = traceback.format_exc()
        print(f"❌ Unexpected Exception during license verification: {error_details}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
