# from main import app
from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    SecurityScopes,
)
from jwt.exceptions import InvalidTokenError
# from pwdlib import PasswordHash
from passlib.context import CryptContext
from jsonmap import TokenData
from pydantic import ValidationError
from sqlalchemy.orm import Session
from sqlalchemy import select
from models import SessionLocal, User


SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

# password_hash = PasswordHash.recommended()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT helpers, password verify, etc.


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# def get_password_hash(password:str):
#     return pwd_context.hash(password)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Read information about the current user.",
            "items": "Read items."},
)


# def verify_password(plain_password, hashed_password):
#     return password_hash.verify(plain_password, hashed_password)


# def get_password_hash(password):
#     return password_hash.hash(password)


def get_user_by_email(db, email: str):
    if email in db:
        user_dict = db[email]
        return db.scalar(select(User).where(User.email == email))


def authenticate_user(db: Session, email: str, plain_password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(plain_password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

db = SessionLocal()
users = db.scalars(select(User)).all()

for u in users:
    if not u.password.startswith("$2b$"):  # bcrypt hashes start with $2b$
        u.password = pwd_context.hash(u.password)
db.commit()
db.close()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_by_email(db: Session, email: str):
    return db.scalar(select(User).where(User.email == email))


async def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        scope_str: str = payload.get("scope", "")
        token_scopes = scope_str.split(" ")
        token_data = TokenData(scopes=token_scopes, username=email)
    except (InvalidTokenError, ValidationError):
        raise credentials_exception
    user = db.scalar(select(User).where(User.email == token_data.username))
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Security(get_current_user, scopes=["me"])],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
