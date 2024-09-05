from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class UserBase(BaseModel):
    name: str

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

class StockInBase(BaseModel):
    stock_in_date: date
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

class SaleItemBase(BaseModel):
    product_id: int
    quantity: int

class SaleBase(BaseModel):
    date: date
    items: List[SaleItemBase]

class Sale(SaleBase):
    id: int

    class Config:
        orm_mode = True

class InvoiceBase(BaseModel):
    sale_id: int
    amount: float
    date: date

class Invoice(InvoiceBase):
    id: int

    class Config:
        orm_mode = True

class PaymentBase(BaseModel):
    amount: float
    date: date
    invoice_id: int

class Payment(PaymentBase):
    id: int

    class Config:
        orm_mode = True
