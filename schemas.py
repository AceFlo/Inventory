from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    name: str
    email: str
    contact_no: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    product_name: str
    price: float
    description: Optional[str] = None


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True


class CustomerBase(BaseModel):
    name: str
    address: str
    phone: str


class Customer(CustomerBase):
    id: int

    class Config:
        orm_mode = True


class InvoiceBase(BaseModel):
    invoice_date: datetime
    total_amount: float
    gst: float
    discount: float
    user_id: int
    customer_id: int


class Invoice(InvoiceBase):
    id: int

    class Config:
        orm_mode = True


class PaymentBase(BaseModel):
    amount: float
    payment_date: datetime
    profit_loss: float
    user_id: int
    customer_id: int


class Payment(PaymentBase):
    id: int

    class Config:
        orm_mode = True


class StockInBase(BaseModel):
    stock_in_date: datetime
    quantity: int
    product_id: int
    user_id: int
    customer_id: int


class StockIn(StockInBase):
    id: int

    class Config:
        orm_mode = True


class RemainingStockBase(BaseModel):
    product_id: int
    quantity: int


class RemainingStock(RemainingStockBase):
    id: int

    class Config:
        orm_mode = True
