from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserPostRegister(BaseModel):
    name: str
    phone: str
    email: EmailStr
    # full_name: str | None = None
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


class SaleDetailsItem(BaseModel):
    product_id: int
    quantity: float


class SalePostMap(BaseModel):
    details: list[SaleDetailsItem]


class SaleGetMap(SalePostMap):
    id: int


# class Products(BaseModel):
#     name: str
#     buying_price: float
#     selling_price: float
#     model: str
#     year: int
#     condition: str
#     fuel: str


class PurchasePostMap(BaseModel):
    product_id: int
    quantity: float


class PurchaseGetMap(PurchasePostMap):
    id: int
    product: ProductGetMap


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
