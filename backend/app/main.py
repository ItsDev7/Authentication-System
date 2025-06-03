# main.py
"""
Main entry point for the FastAPI backend application.
Sets up the FastAPI app, includes routers, and defines startup events.
"""

from fastapi import FastAPI

# Import routers from the routes directory
from .routes.login import router as login_router
from .routes.signup import router as signup_router
from .routes.verify_license import router as verify_license_router
from .routes.license import router as license_router

# Import models to ensure they are known to SQLAlchemy/Alembic
# This import is necessary for Alembic autogenerate to detect model changes.
import app.models

# Initialize the FastAPI application
app = FastAPI(
    title="Authentication System Backend",
    description="FastAPI backend for the user authentication and licensing system.",
    version="1.0.0",
    # Add other metadata as needed
)

# Include the routers to add their endpoints to the application
app.include_router(login_router)
app.include_router(signup_router)
app.include_router(verify_license_router)
app.include_router(license_router) # Include the license router

# Define a startup event handler
@app.on_event("startup")
async def on_startup():
    """Handles actions to be performed when the application starts up."""
    pass 

