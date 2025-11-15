from passlib.context import CryptContext
from src.config import Settings


# Создаем контекст для хеширования паролей
pwd_context = CryptContext(schemes=[Settings.PASSWORD_HASH_ALGORITHM], deprecated="auto")


class PasswordService:
    """Сервис для работы с паролями (хеширование и проверка)"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Хеширует пароль с использованием bcrypt
        
        Args:
            password: Пароль в открытом виде
        
        Returns:
            Хешированный пароль
        """
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Проверяет, соответствует ли пароль хешу
        
        Args:
            plain_password: Пароль в открытом виде
            hashed_password: Хешированный пароль из базы данных
        
        Returns:
            True, если пароль верный, иначе False
        """
        return pwd_context.verify(plain_password, hashed_password)

