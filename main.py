# from typing import Union
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status
from models import Base, engine, Product, SessionLocal, Sale,  User, Purchase
from jsonmap import ProductGetMap, SaleGetMap, UserGetRegister, PurchaseGetMap, SalePostMap, UserPostLogin, UserPostRegister, Token
from sqlalchemy import select
from werkzeug.security import  check_password_hash
from datetime import datetime, timedelta, timezone
from myjwt import create_access_token, get_db
from passlib.context import CryptContext



app = FastAPI()
ACCESS_TOKEN_EXPIRE_MINUTES = 30 

# create tables on startup


@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"Duka FastAPI": "1.0"}

def get_password_hash(password:str):
    return pwd_context.hash(password)

@app.post("/register", response_model=UserGetRegister)
def register_user(user: UserPostRegister, db:Session = Depends(get_db)):
    # db = SessionLocal()
    # check email
    if db.scalar(select(User).where(User.email == user.email)):
        raise HTTPException(status_code=400, detail="Email already registered")
    # check phone
    if db.scalar(select(User).where(User.phone == user.phone)):
        raise HTTPException(status_code=400, detail="Phone already registered")
    new_user = User(
        name=user.name,
        phone=user.phone,
        email=user.email,
        password=get_password_hash(user.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post("/login", response_model=Token)
def login_user(user: UserPostLogin, db: Session = Depends(get_db)):
    # db = SessionLocal()
    db_user = db.scalar(select(User).where(User.email == user.email))
    if not db_user:
        raise HTTPException(
            status_code=401, detail="Invalid email or password")
    if not pwd_context.verify(user.password, db_user.password):
        raise HTTPException(
            status_code=401, detail="Invalid email or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")

    # return {
    #     "message": "Login successful",
    #     "user_id": db_user.id,
    #     "email": db_user.email
    # }
# ensure sessions close properly


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/users", response_model=list[UserGetRegister])
def get_users(db: Session = Depends(get_db)):
    users = db.scalars(select(User)).all()
    return users


@app.get("/products", response_model=list[ProductGetMap])
def get_products():
    prods = select(Product)
    return SessionLocal.scalars(prods)


@app.get("/products", response_model=ProductGetMap)
def create_product(json_product_obj: ProductGetMap):
    model_obj = Product(
        name=json_product_obj.name,
        buying_price=json_product_obj.buying_price,
        selling_price=json_product_obj.selling_price
    )
    SessionLocal.add(model_obj)
    SessionLocal.commit()
    return model_obj


@app.get("/sales", response_model=list[SaleGetMap])
def get_sales():
    sales = select(Sale).join(Sale.details)
    return SessionLocal.scalars(sales)


@app.get("/sales", response_model=SaleGetMap)
def create_sale(json_sale_obj: SalePostMap):
    model_obj = Sale(
        product_id=json_sale_obj.product_id,
        quantity=json_sale_obj.quantity
    )
    SessionLocal.add(model_obj)
    SessionLocal.commit()
    return model_obj


@app.get("/purchase", response_model=list[PurchaseGetMap])
def get_purchases():
    purchase = select(Purchase)
    return SessionLocal.scalars(purchase)
