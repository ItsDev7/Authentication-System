"""
Router for user signup.
Provides an endpoint to register new users.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# Local imports
from ..schemas.schema import UserCreate
from ..models.models import User
from ..core.database import get_db
from ..core.hashing import hash_password

# Create an API router
router = APIRouter()

@router.post("/signup/")
async def signup(
    user: UserCreate, # User details for registration (username and password)
    db: AsyncSession = Depends(get_db) # Database session dependency
):
    """
    Registers a new user.
    Checks if the username already exists and hashes the password before saving.
    """
    try:
        # Check if a user with the provided username already exists
        existing_user_query = await db.execute(select(User).where(User.username == user.username))
        existing_user = existing_user_query.scalars().first()

        # If user exists, raise a conflict error
        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")

        # Hash the user's password for secure storage
        hashed_password = hash_password(user.password)

        # Create a new User instance
        new_user = User(
            username=user.username,
            password=hashed_password,
            is_active=False  # New accounts are inactive by default, pending activation (e.g., via license)
        )
        
        # Add the new user to the database session
        db.add(new_user)
        # Flush the session to get the new user's ID (if needed, though not used here)
        await db.flush()
        # Commit the transaction to save the new user to the database
        await db.commit()
        # Refresh the new user object to get updated attributes (like ID)
        await db.refresh(new_user)

        # Return a success message
        return {"message": "User Created Successfully", "user_id": new_user.id}

    # Catch specific HTTPExceptions raised within the try block
    except HTTPException as http_err:
        raise http_err
        
    # Catch any other unexpected exceptions
    except Exception as e:
        # Log the full traceback for debugging server-side (not returned to user)
        import traceback
        error_details = traceback.format_exc()
        print(f"❌ Unexpected Exception during signup: {error_details}")
        # Return a generic internal server error to the user
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error")
