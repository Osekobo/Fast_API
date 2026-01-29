from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import timedelta
from models import Base, engine, Product, Sale, User, Purchase
from jsonmap import (
    ProductGetMap,
    SaleGetMap,
    SalePostMap,
    UserGetRegister,
    UserPostRegister,
    UserPostLogin,
    PurchaseGetMap,
    Token,
)
from myjwt import (
    get_db,
    get_password_hash,
    verify_password,
    create_access_token,
)

app = FastAPI()
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Create tables on startup
@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"Duka FastAPI": "Version 1.0"}


# Register
@app.post("/register", response_model=UserGetRegister)
def register_user(user: UserPostRegister, db: Session = Depends(get_db)):
    if db.scalar(select(User).where(User.email == user.email)):
        raise HTTPException(status_code=400, detail="Email already registered")

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

# Login
@app.post("/login", response_model=Token)
def login_user(user: UserPostLogin, db: Session = Depends(get_db)):
    db_user = db.scalar(select(User).where(User.email == user.email))
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    access_token = create_access_token(
        data={"sub": db_user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return Token(access_token=access_token, token_type="bearer")


# Users
@app.get("/users", response_model=list[UserGetRegister])
def get_users(db: Session = Depends(get_db)):
    return db.scalars(select(User)).all()


# Products
@app.get("/products", response_model=list[ProductGetMap])
def get_products(db: Session = Depends(get_db)):
    return db.scalars(select(Product)).all()


@app.post("/products", response_model=ProductGetMap)
def create_product(product: ProductGetMap, db: Session = Depends(get_db)):
    model = Product(**product.dict())
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


# Sales
@app.get("/sales", response_model=list[SaleGetMap])
def get_sales(db: Session = Depends(get_db)):
    return db.scalars(select(Sale)).all()


@app.post("/sales", response_model=SaleGetMap)
def create_sale(sale: SalePostMap, db: Session = Depends(get_db)):
    model = Sale(**sale.dict())
    db.add(model)
    db.commit()
    db.refresh(model)
    return model


# Purchases
@app.get("/purchase", response_model=list[PurchaseGetMap])
def get_purchases(db: Session = Depends(get_db)):
    return db.scalars(select(Purchase)).all()
