"""
Router for user login.
Provides an endpoint to authenticate users.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..schemas.schema import UserCreate
from ..models.models import User
from ..core.database import get_db
from ..core.hashing import verify_password
from datetime import datetime, UTC # Import UTC for timezone-aware comparison
import traceback
from fastapi.responses import JSONResponse

# Create an API router
router = APIRouter()

@router.post("/login/")
async def login(
    user: UserCreate, # User credentials (username and password)
    db: AsyncSession = Depends(get_db) # Database session dependency
):
    """
    Authenticates a user based on username and password.
    Checks for account activation and subscription expiration.
    """
    try:
        # Find the user in the database by username
        result = await db.execute(select(User).where(User.username == user.username))
        db_user = result.scalars().first()

        # If user not found, raise authentication error
        if not db_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

        # Verify the provided password against the stored hashed password
        if not verify_password(user.password, db_user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")

        # --- Account Status Checks ---
        # Check if the account is active (based on is_active flag)
        if not db_user.is_active:
             return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={
                    "detail": "Account not activated. Please enter activation code.",
                    "user_id": db_user.id
                }
            )

        # Check if the active account has an expired subscription
        # Compare timezone-aware datetimes
        if db_user.expiration_date:
            # Make the database datetime timezone-aware (assuming it's stored as UTC naive)
            aware_expiration_date = db_user.expiration_date.replace(tzinfo=UTC)
            if aware_expiration_date < datetime.now(UTC):
                # If expired, mark account as inactive and clear expiration date
                db_user.is_active = False # Use Boolean False
                db_user.expiration_date = None
                await db.commit()
                # Return expired subscription message
                return JSONResponse(
                    status_code=status.HTTP_403_FORBIDDEN,
                    content={
                        "detail": "Subscription expired. Please renew your license.",
                        "user_id": db_user.id
                    }
                )

        # If all checks pass, login is successful
        return {
            "message": "Login Successful",
            "expiration_date": db_user.expiration_date.isoformat() if db_user.expiration_date else None
        }

    # Catch specific HTTPExceptions raised within the try block
    except HTTPException as http_exc:
        raise http_exc

    # Catch any other unexpected exceptions
    except Exception as e:
        # Log the full traceback for debugging server-side (not returned to user)
        error_details = traceback.format_exc()
        print(f"❌ Unexpected Exception during login: {error_details}")
        # Return a generic internal server error to the user
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
