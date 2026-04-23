from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, Security, status, Request
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import SessionLocal, User
from jsonmap import TokenData

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login",
    scopes={
        "me": "Read information about the current user",
        "items": "Read items",
    },
)

# Database dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Hash password
def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_user_by_email(db: Session, email: str):
    return db.scalar(select(User).where(User.email == email))


# create access token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=15)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# from fastapi import Request, Depends, HTTPException, status


async def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    token = request.cookies.get("access_token")
    print("TOKEN:", token)

    if not token:
        raise credentials_exception

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("PAYLOAD:", payload)

        email = payload.get("sub")
        if not email:
            raise credentials_exception

    except Exception as e:
        print("JWT ERROR:", e)
        raise credentials_exception

    user = get_user_by_email(db, email)

    if not user:
        raise credentials_exception

    return user
