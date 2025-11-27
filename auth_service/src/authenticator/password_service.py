from passlib.context import CryptContext
from src.config import Settings


# Create a hashing context for passwords
pwd_context = CryptContext(schemes=[Settings.PASSWORD_HASH_ALGORITHM], deprecated="auto")


class PasswordService:
    """Password utilities (hashing and verification)"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hashes a password using bcrypt
        
        Args:
            password: Plain-text password
        
        Returns:
            Hashed password
        """
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Checks whether a password matches its hash
        
        Args:
            plain_password: Plain-text password
            hashed_password: Hashed password from storage
        
        Returns:
            True if the password matches, otherwise False
        """
        return pwd_context.verify(plain_password, hashed_password)

