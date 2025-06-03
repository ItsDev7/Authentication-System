# config.py
"""
Module for loading application settings from environment variables.
Uses pydantic-settings to validate and provide structured access to settings.
"""

from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Determine the path to the .env file relative to the current file
env_path = Path(__file__).parent.parent.parent / ".env"
# Load environment variables from the specified .env file
load_dotenv(dotenv_path=env_path)

# Define a Settings class using pydantic_settings.BaseSettings
# This class automatically loads environment variables based on the defined fields.
class Settings(BaseSettings):
    # Database connection URL loaded from the DATABASE_URL environment variable
    DATABASE_URL: str

    # Inner Config class to specify settings for BaseSettings
    class Config:
        # Specify the name of the environment file to load
        env_file = ".env"

# Create an instance of the Settings class
settings = Settings()
