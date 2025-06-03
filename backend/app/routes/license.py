"""
Router for managing license codes.
Provides endpoints for listing, generating, validating, and activating licenses.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

# Local imports
from ..core.database import get_db
from app.services.license_service import LicenseService
from app.schemas.schema import LicenseCodeResponse
from app.models.models import LicenseCode

# Create an API router with a prefix and tags
router = APIRouter(prefix="/license", tags=["license"])

@router.get("/list", response_model=List[LicenseCodeResponse])
async def list_license_codes(
    db: AsyncSession = Depends(get_db), # Database session dependency
    skip: int = 0, # Pagination: number of items to skip
    limit: int = 100 # Pagination: maximum number of items to return
):
    """List all license codes available in the system."""
    # Select license codes from the database with pagination
    result = await db.execute(select(LicenseCode).offset(skip).limit(limit))
    codes = result.scalars().all()
    return codes

@router.post("/generate", response_model=LicenseCodeResponse)
async def generate_license_code(
    duration_days: int = 30, # Duration of the license in days
    db: AsyncSession = Depends(get_db) # Database session dependency
):
    """Generate a single new license code with a specified duration."""
    try:
        # Delegate code generation logic to the LicenseService
        license_code = await LicenseService.create_license_code(db, duration_days)
        return license_code
    except Exception as e:
        # Catch any exceptions during generation and return a 500 error
        # TODO: Consider more specific exception handling if possible
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-batch", response_model=List[LicenseCodeResponse])
async def generate_multiple_codes(
    count: int = 5, # Number of license codes to generate
    duration_days: int = 30, # Duration for each license code in days
    db: AsyncSession = Depends(get_db) # Database session dependency
):
    """Generate multiple license codes at once."""
    try:
        codes = []
        # Loop to generate the specified number of codes
        for _ in range(count):
            code = await LicenseService.create_license_code(db, duration_days)
            codes.append(code)
        return codes
    except Exception as e:
        # Catch any exceptions during batch generation and return a 500 error
        # TODO: Consider more specific exception handling if possible
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/validate/{code}")
async def validate_license_code(
    code: str, # The license code to validate
    db: AsyncSession = Depends(get_db) # Database session dependency
):
    """Validate if a given license code is valid, unused, and not expired."""
    # Delegate validation logic to the LicenseService
    is_valid, message, expires_at = await LicenseService.validate_code(db, code)
    if not is_valid:
        # Return a 400 error if the code is invalid
        raise HTTPException(status_code=400, detail=message)
    # Return validation success with details
    return {"is_valid": is_valid, "message": message, "expires_at": expires_at}

@router.post("/activate/{code}")
async def activate_license_code(
    code: str, # The license code to activate
    user_id: int, # The ID of the user activating the code
    db: AsyncSession = Depends(get_db) # Database session dependency
):
    """Activate a license code for a specific user."""
    # Delegate activation logic to the LicenseService
    success, message, expires_at = await LicenseService.activate_code(db, code, user_id)
    if not success:
        # Return a 400 error if activation fails
        raise HTTPException(status_code=400, detail=message)
    # Return activation success with details
    return {"message": message, "expires_at": expires_at}