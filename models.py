from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import String, Float, Integer, DateTime, create_engine
from typing import List
# from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime


DATABASE_URL = "postgresql://postgres:12039@localhost:5432/fast_api"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False)

    buying_price: Mapped[float] = mapped_column(Float, nullable=False)
    selling_price: Mapped[float] = mapped_column(Float, nullable=False)

    model: Mapped[str] = mapped_column(String, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    condition: Mapped[str] = mapped_column(String, nullable=False)
    fuel: Mapped[str] = mapped_column(String, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    purchases: Mapped[List["Purchase"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan"
    )

class Sale(Base):
    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationship with SalesDetails
    details: Mapped[List["SalesDetails"]] = relationship(
        back_populates="sale",
        cascade="all, delete-orphan"
    )


class SalesDetails(Base):
    __tablename__ = "sales_details"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    sale_id: Mapped[int] = mapped_column(
        ForeignKey("sales.id"), nullable=False
    )

    product_id: Mapped[int] = mapped_column(Integer, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    # Relationship back to Sale
    sale: Mapped["Sale"] = relationship(back_populates="details")


class Purchase(Base):
    __tablename__ = "purchases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    quantity: Mapped[float] = mapped_column(Float, nullable=False)

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"), nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationship to Product
    product: Mapped["Product"] = relationship(back_populates="purchases")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    phone: Mapped[str] = mapped_column(String(256), unique=True,nullable=False)
    email: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(256), nullable=False)  # hashed password
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
