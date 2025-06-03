# hashing.py
"""
Module for password hashing and verification.
Uses passlib with the bcrypt scheme.
"""

from passlib.context import CryptContext

# Define the CryptContext with the bcrypt hashing scheme
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hashes a given plain password using the configured CryptContext."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against a hashed password using the configured CryptContext."""
    return pwd_context.verify(plain_password, hashed_password)
# print(hash_password("1")) # Removed: Testing line
