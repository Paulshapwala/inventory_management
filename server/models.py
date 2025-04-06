import sys
import os
# Add the parent directory containing 'app' to your path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship, sessionmaker, Mapped, mapped_column
from sqlalchemy.sql import func
from server.setup import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id:Mapped[int] = mapped_column(primary_key=True)
    username:Mapped[str] = mapped_column(String(64))
    isAdmin:Mapped[bool]
       # relationships
    password:Mapped["Password"] = relationship(back_populates="user",uselist=False,cascade="all, delete-orphan")
    transactions:Mapped[list["Transaction"]] = relationship(back_populates="user")

    def __repr__(self):
       return f"user:{self.username!r} id:{self.id!r} admin:{self.isAdmin!r} pass:{self.password!r}"
    

class Password(Base):
    __tablename__ = "passwords"
    id:Mapped[int]  = mapped_column(primary_key=True)
    password_hash:Mapped[str] = mapped_column(String(64))
    userId:Mapped[int] = mapped_column(ForeignKey("users.id",ondelete="CASCADE"))
    # relationships
    user:Mapped["User"] = relationship(back_populates="password", uselist=False)
    def __repr__(self):
        return f"{self.password_hash!r}"


class Product(Base):
    __tablename__ = "products"
    id:Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(64))
    category:Mapped[str] = mapped_column(String(32))
    quantity:Mapped[int]
    price:Mapped[float]

    # relationships
    transactionitems:Mapped[list["TransactionItem"]] = relationship(back_populates="product")
    
    def __repr__(self):
        return f"productId:{self.id!r} name:{self.name!r} category:{self.category!r}"
    

class Transaction(Base):
    __tablename__ = "transactions"
    id:Mapped[int] = mapped_column(primary_key=True)
    userId:Mapped[int] = mapped_column(ForeignKey("users.id"))
    timeStamp:Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    # relationships
    items: Mapped[list["TransactionItem"]] = relationship(back_populates="transaction", cascade="all, delete-orphan")
    user:Mapped["User"] = relationship(back_populates="transactions")

    def __repr__(self):
        return f"transactionId:{self.id!r} time:{self.timeStamp!r}"

class TransactionItem(Base):
    __tablename__ = "transactionItems"
    id:Mapped[int] = mapped_column(primary_key=True)
    productId:Mapped[int] = mapped_column(ForeignKey("products.id"))
    transactionId:Mapped[int] = mapped_column(ForeignKey("transactions.id"))
    priceAtTime:Mapped[float]
    quantity:Mapped[int]
    # relationships
    product:Mapped["Product"] = relationship(back_populates="transactionitems")
    transaction:Mapped["Transaction"] = relationship(back_populates="items")

    def __repr__(self):
        return f"itemId:{self.id!r} quantity:{self.quantity!r} price:{self.priceAtTime!r}"

