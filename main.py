import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, engine
import models
import functions
from schemas import (
    User, UserBase, ProductBase, Product,
    CustomerBase, Customer, StockInBase, StockIn,
    RemainingStockBase, RemainingStock, InvoiceBase, Invoice,
    PaymentBase, Payment, SaleBase, SaleItemBase
)

app = FastAPI()

# User routes
@app.post("/users/", response_model=User)
def create_user(user_data: UserBase, db_session: Session = Depends(get_db)):
    db_user = models.User(**user_data.dict())
    db_session.add(db_user)
    db_session.commit()
    db_session.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db_session: Session = Depends(get_db)):
    db_user = db_session.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Product routes
@app.post("/products/", response_model=Product)
def create_product(product_data: ProductBase, db_session: Session = Depends(get_db)):
    db_product = models.Product(**product_data.dict())
    db_session.add(db_product)
    db_session.commit()
    db_session.refresh(db_product)
    return db_product

@app.get("/products/{product_id}", response_model=Product)
def read_product(product_id: int, db_session: Session = Depends(get_db)):
    db_product = db_session.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.put("/products/{product_id}", response_model=Product)
def update_product(product_id: int, product_data: ProductBase, db_session: Session = Depends(get_db)):
    db_product = db_session.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    if product_data.product_name is not None:
        db_product.product_name = product_data.product_name
    if product_data.price is not None:
        db_product.price = product_data.price
    if product_data.description is not None:
        db_product.description = product_data.description

    db_session.commit()
    db_session.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}", response_model=Product)
def delete_product(product_id: int, db_session: Session = Depends(get_db)):
    db_product = db_session.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    db_session.delete(db_product)
    db_session.commit()
    return db_product

# Customer routes
@app.post("/customers/", response_model=Customer)
def create_customer(customer_data: CustomerBase, db_session: Session = Depends(get_db)):
    db_customer = models.Customer(**customer_data.dict())
    db_session.add(db_customer)
    db_session.commit()
    db_session.refresh(db_customer)
    return db_customer

@app.get("/customers/{customer_id}", response_model=Customer)
def read_customer(customer_id: int, db_session: Session = Depends(get_db)):
    db_customer = db_session.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return db_customer

# Stock In routes
@app.post("/stock-in/", response_model=StockIn)
def create_stock_in(stock_in_data: StockInBase, db_session: Session = Depends(get_db)):
    return functions.create_stock_in(db_session, stock_in_data)

# Sale routes
@app.post("/sales/", response_model=Sale)
def create_sale(sale_data: SaleBase, db_session: Session = Depends(get_db)):
    try:
        sale, invoice = functions.create_sale(db_session, sale_data)
        return {"sale": sale, "invoice": invoice}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Invoice routes
@app.get("/invoices/{invoice_id}", response_model=Invoice)
def read_invoice(invoice_id: int, db_session: Session = Depends(get_db)):
    db_invoice = db_session.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if db_invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return db_invoice

# Payment routes
@app.post("/payments/", response_model=Payment)
def create_payment(payment_data: PaymentBase, db_session: Session = Depends(get_db)):
    db_payment = models.Payment(**payment_data.dict())
    db_session.add(db_payment)
    db_session.commit()
    db_session.refresh(db_payment)
    return db_payment

if __name__ == "__main__":
    models.Base.metadata.create_all(bind=engine)
    uvicorn.run(app, host="0.0.0.0", port=8000)
