from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserPostRegister(BaseModel):
    name: str
    phone: str
    email: EmailStr
    password: str


class UserPostLogin(BaseModel):
    email: EmailStr
    password: str


class UserGetRegister(BaseModel):
    id: int
    name: str
    phone: str
    email: EmailStr


class ProductPostMap(BaseModel):
    name: str
    buying_price: float
    selling_price: float
    model: str
    year: int
    condition: str
    fuel: str


class ProductGetMap(ProductPostMap):
    id: int


class RemainingPerProductMap(BaseModel):
    product_id: int
    product_name: str
    remaining_quantity: float


class SaleDetailsItem(BaseModel):
    product_id: int
    quantity: float


class SalePostMap(BaseModel):
    details: list[SaleDetailsItem]


class SaleGetMap(SalePostMap):
    id: int


class SalePerProductMap(BaseModel):
    sale_id: int
    product_id: int
    quantity: float
    created_at: datetime


class PurchasePostMap(BaseModel):
    product_id: int
    quantity: float


class PurchaseGetMap(PurchasePostMap):
    id: int
    quantity: float
    product_id: int
    created_at: datetime
    updated_at: datetime


# class UserPostRegister(BaseModel):
#     name: str | None = None
#     phone: str
#     email: str
#     password: str


# class UserGetRegister(UserPostRegister):
#     id: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
    scopes: list[str] = []
