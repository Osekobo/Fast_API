from pydantic import BaseModel


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


class UserPostMap(BaseModel):
    name: str
    phone: str
    email: str
    password: str


class UserGetMap(UserPostMap):
    id: int
