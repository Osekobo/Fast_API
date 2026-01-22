# from typing import Union

from fastapi import FastAPI
from models import Base, engine, Product, SessionLocal, Sale,  User, Purchase
from jsonmap import ProductGetMap, SaleGetMap, UserGetMap, PurchaseGetMap
from sqlalchemy import select

app = FastAPI()

# create tables on startup


@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"Duka FastAPI": "1.0"}

# uvicorn main:app --reload
# http://127.0.0.1:8000/docs


@app.get("/products", response_model=list[ProductGetMap])
def get_products():
    prods = select(Product)
    return SessionLocal.scalars(prods)


@app.get("/sales", response_model=list[SaleGetMap])
def get_sales():
    sales = select(Sale).join(Sale.details)
    return SessionLocal.scalars(sales)


@app.get("/purchase", response_model=list[PurchaseGetMap])
def get_purchases():
    purchase = select(Purchase)
    return SessionLocal.scalars(purchase)


@app.get("/users", response_model=list[UserGetMap])
def get_users():
    usr = select(User)
    return SessionLocal.scalars(usr)
