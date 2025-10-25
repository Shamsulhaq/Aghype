from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from backend.config import settings


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(subject: str, expires_delta: int = None):
    expire = datetime.utcnow() + timedelta(minutes=(expires_delta or settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = {"sub": str(subject), "exp": expire}
    encoded = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded


# def create_refresh_token(subject: str, expires_delta: int = None):
#     expire = datetime.utcnow() + timedelta(days=7)  # Refresh tokens last for 7 days
#     to_encode = {"sub": str(subject), "exp": expire}
#     encoded = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
#     return encoded


def decode_token(token: str):
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    print(payload)
    return payload


# def verify_refresh_token(token: str):
#     try:
#         payload = decode_token(token)
#     except Exception:
#         return None
#     if payload.get('type') != 'refresh':
#         raise JWTError('Not a refresh token')
#     return payload

#TODO:: have to add refresh token functions