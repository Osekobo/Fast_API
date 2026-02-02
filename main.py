from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from datetime import timedelta
from models import Base, engine, Product, Sale, User, Purchase, SalesDetails
from typing import List
from jsonmap import (
    ProductGetMap,
    SaleGetMap,
    SalePostMap,
    UserGetRegister,
    UserPostRegister,
    UserPostLogin,
    PurchaseGetMap,
    PurchasePostMap,
    SalePerProductMap,
    SaleDetailsItem,
    Token,
)
from myjwt import (
    get_db,
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
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
def create_sale(
    sale: SalePostMap,
    db: Session = Depends(get_db)
):
    model = Sale()

    for item in sale.details:
        model.details.append(
            SalesDetails(
                product_id=item.product_id,
                quantity=item.quantity
            )
        )

    db.add(model)
    db.commit()
    db.refresh(model)
    return model


# Purchases
@app.get("/purchase", response_model=list[PurchaseGetMap])
def get_purchases(db: Session = Depends(get_db)):
    return db.scalars(select(Purchase)).all()


@app.post("/purchase", response_model=PurchaseGetMap, status_code=201)
def create_purchase(
    purchase: PurchasePostMap,
    db: Session = Depends(get_db)
):
    new_purchase = Purchase(
        quantity=purchase.quantity,
        product_id=purchase.product_id
    )

    db.add(new_purchase)
    db.commit()
    db.refresh(new_purchase)

    return new_purchase

# Dashboard


@app.get("/dashboard/spp", response_model=List[SalePerProductMap])
def get_sales_per_product(
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user),
):
    sales_data = db.execute(
        select(
            SalesDetails.product_id,  # ✅ ORM model
            Product.name.label("product_name"),
            func.sum(SalesDetails.quantity).label("total_quantity_sold"),
            func.sum(
                SalesDetails.quantity * Product.selling_price
            ).label("total_sales_amount")
        )
        .join(Product, SalesDetails.product_id == Product.id)
        .join(Sale, SalesDetails.sale_id == Sale.id)
        .group_by(SalesDetails.product_id, Product.name)
    ).all()

    return [
        SalePerProductMap(
            product_id=row.product_id,
            product_name=row.product_name,
            total_quantity_sold=row.total_quantity_sold,
            total_sales_amount=row.total_sales_amount,
        )
        for row in sales_data
    ]


@app.get("/dashboard/rpp", response_model=List[SalePerProductMap])
def get_remaining_per_product(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    purchased_subq = (
        select(
            Purchase.product_id.label("product_id"),
            func.sum(Purchase.quantity).label("total_purchased")
        )
        .group_by(Purchase.product_id)
        .subquery()
    )

    sold_subq = (
        select(
            SaleDetailsItem.product_id.label("product_id"),
            func.sum(SaleDetailsItem.quantity).label("total_sold")
        )
        .group_by(SaleDetailsItem.product_id)
        .subquery()
    )

    data = db.execute(
        select(
            Product.id.label("product_id"),
            Product.name.label("product_name"),
            (
                func.coalesce(purchased_subq.c.total_purchased, 0)
                - func.coalesce(sold_subq.c.total_sold, 0)
            ).label("remaining_quantity")
        )
        .outerjoin(purchased_subq, Product.id == purchased_subq.c.product_id)
        .outerjoin(sold_subq, Product.id == sold_subq.c.product_id)
    ).all()

    return [
        SalePerProductMap(
            product_id=row.product_id,
            product_name=row.product_name,
            total_quantity_sold=row.remaining_quantity,
            total_sales_amount=0,  # not applicable here
        )
        for row in data
    ]


# ---------------- LOGIN (OAUTH2 – SWAGGER) ----------------
# @router.post("/token", tags=["auth"])
# def login_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     token = create_access_token(user.email)
#     return {
#         "access_token": token,
#         "token_type": "bearer",
#     }
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")
