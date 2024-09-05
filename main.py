import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models
import functions
from schemas import (
    User, UserBase, ProductBase, Product,
    CustomerBase, Customer, InvoiceBase, Invoice,
    PaymentBase, Payment, StockIn, StockInBase,
    RemainingStock, RemainingStockBase
)
from database import get_db, engine

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


@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user_data: UserBase, db_session: Session = Depends(get_db)):
    db_user = db_session.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if user_data.name is not None:
        db_user.name = user_data.name
    if user_data.email is not None:
        db_user.email = user_data.email
    if user_data.contact_no is not None:
        db_user.contact_no = user_data.contact_no

    db_session.commit()
    db_session.refresh(db_user)
    return db_user


@app.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: int, db_session: Session = Depends(get_db)):
    db_user = db_session.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_session.delete(db_user)
    db_session.commit()
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


@app.put("/customers/{customer_id}", response_model=Customer)
def update_customer(customer_id: int, customer_data: CustomerBase, db_session: Session = Depends(get_db)):
    db_customer = db_session.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    if customer_data.name is not None:
        db_customer.name = customer_data.name
    if customer_data.address is not None:
        db_customer.address = customer_data.address
    if customer_data.phone is not None:
        db_customer.phone = customer_data.phone

    db_session.commit()
    db_session.refresh(db_customer)
    return db_customer


@app.delete("/customers/{customer_id}", response_model=Customer)
def delete_customer(customer_id: int, db_session: Session = Depends(get_db)):
    db_customer = db_session.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if db_customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")

    db_session.delete(db_customer)
    db_session.commit()
    return db_customer


# Stock In routes
@app.post("/stock-in/", response_model=StockIn)
def create_stock_in(stock_in_data: StockInBase, db_session: Session = Depends(get_db)):
    return functions.create_stock_in(db=db_session, stock_in=stock_in_data)


@app.get("/stock-in/{stock_in_id}", response_model=StockIn)
def read_stock_in(stock_in_id: int, db_session: Session = Depends(get_db)):
    db_stock_in = db_session.query(models.StockIn).filter(models.StockIn.id == stock_in_id).first()
    if db_stock_in is None:
        raise HTTPException(status_code=404, detail="Stock In not found")
    return db_stock_in


@app.put("/stock-in/{stock_in_id}", response_model=StockIn)
def update_stock_in(stock_in_id: int, stock_in_data: StockInBase, db_session: Session = Depends(get_db)):
    db_stock_in = db_session.query(models.StockIn).filter(models.StockIn.id == stock_in_id).first()
    if db_stock_in is None:
        raise HTTPException(status_code=404, detail="Stock In not found")

    if stock_in_data.stock_in_date is not None:
        db_stock_in.stock_in_date = stock_in_data.stock_in_date
    if stock_in_data.quantity is not None:
        db_stock_in.quantity = stock_in_data.quantity
    if stock_in_data.product_id is not None:
        db_stock_in.product_id = stock_in_data.product_id
    if stock_in_data.user_id is not None:
        db_stock_in.user_id = stock_in_data.user_id
    if stock_in_data.customer_id is not None:
        db_stock_in.customer_id = stock_in_data.customer_id

    db_session.commit()
    db_session.refresh(db_stock_in)
    return db_stock_in


@app.delete("/stock-in/{stock_in_id}", response_model=StockIn)
def delete_stock_in(stock_in_id: int, db_session: Session = Depends(get_db)):
    db_stock_in = db_session.query(models.StockIn).filter(models.StockIn.id == stock_in_id).first()
    if db_stock_in is None:
        raise HTTPException(status_code=404, detail="Stock In not found")

    db_session.delete(db_stock_in)
    db_session.commit()
    return db_stock_in


# Remaining Stock routes
@app.post("/remaining-stock/", response_model=RemainingStock)
def create_remaining_stock(remaining_stock_data: RemainingStockBase, db_session: Session = Depends(get_db)):
    db_remaining_stock = models.RemainingStock(**remaining_stock_data.dict())
    db_session.add(db_remaining_stock)
    db_session.commit()
    db_session.refresh(db_remaining_stock)
    return db_remaining_stock


@app.get("/remaining-stock/{stock_id}", response_model=RemainingStock)
def read_remaining_stock(stock_id: int, db_session: Session = Depends(get_db)):
    db_remaining_stock = db_session.query(models.RemainingStock).filter(models.RemainingStock.id == stock_id).first()
    if db_remaining_stock is None:
        raise HTTPException(status_code=404, detail="Remaining Stock not found")
    return db_remaining_stock


@app.put("/remaining-stock/{stock_id}", response_model=RemainingStock)
def update_remaining_stock(stock_id: int, remaining_stock_data: RemainingStockBase,
                           db_session: Session = Depends(get_db)):
    db_remaining_stock = db_session.query(models.RemainingStock).filter(models.RemainingStock.id == stock_id).first()
    if db_remaining_stock is None:
        raise HTTPException(status_code=404, detail="Remaining Stock not found")

    if remaining_stock_data.product_id is not None:
        db_remaining_stock.product_id = remaining_stock_data.product_id
    if remaining_stock_data.quantity is not None:
        db_remaining_stock.quantity = remaining_stock_data.quantity

    db_session.commit()
    db_session.refresh(db_remaining_stock)
    return db_remaining_stock


@app.delete("/remaining-stock/{stock_id}", response_model=RemainingStock)
def delete_remaining_stock(stock_id: int, db_session: Session = Depends(get_db)):
    db_remaining_stock = db_session.query(models.RemainingStock).filter(models.RemainingStock.id == stock_id).first()
    if db_remaining_stock is None:
        raise HTTPException(status_code=404, detail="Remaining Stock not found")

    db_session.delete(db_remaining_stock)
    db_session.commit()
    return db_remaining_stock


# Invoice routes
@app.post("/invoices/", response_model=Invoice)
def create_invoice(invoice_data: InvoiceBase, db_session: Session = Depends(get_db)):
    db_invoice = models.Invoice(**invoice_data.dict())
    db_session.add(db_invoice)
    db_session.commit()
    db_session.refresh(db_invoice)
    return db_invoice


@app.get("/invoices/{invoice_id}", response_model=Invoice)
def read_invoice(invoice_id: int, db_session: Session = Depends(get_db)):
    db_invoice = db_session.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if db_invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return db_invoice


@app.put("/invoices/{invoice_id}", response_model=Invoice)
def update_invoice(invoice_id: int, invoice_data: InvoiceBase, db_session: Session = Depends(get_db)):
    db_invoice = db_session.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if db_invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found")

    if invoice_data.total_amount is not None:
        db_invoice.total_amount = invoice_data.total_amount
    if invoice_data.gst is not None:
        db_invoice.gst = invoice_data.gst
    if invoice_data.discount is not None:
        db_invoice.discount = invoice_data.discount
    if invoice_data.user_id is not None:
        db_invoice.user_id = invoice_data.user_id
    if invoice_data.customer_id is not None:
        db_invoice.customer_id = invoice_data.customer_id

    db_session.commit()
    db_session.refresh(db_invoice)
    return db_invoice


@app.delete("/invoices/{invoice_id}", response_model=Invoice)
def delete_invoice(invoice_id: int, db_session: Session = Depends(get_db)):
    db_invoice = db_session.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if db_invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found")

    db_session.delete(db_invoice)
    db_session.commit()
    return db_invoice


# Payment routes
@app.post("/payments/", response_model=Payment)
def create_payment(payment_data: PaymentBase, db_session: Session = Depends(get_db)):
    db_payment = models.Payment(**payment_data.dict())
    db_session.add(db_payment)
    db_session.commit()
    db_session.refresh(db_payment)
    return db_payment


@app.get("/payments/{payment_id}", response_model=Payment)
def read_payment(payment_id: int, db_session: Session = Depends(get_db)):
    db_payment = db_session.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return db_payment


@app.put("/payments/{payment_id}", response_model=Payment)
def update_payment(payment_id: int, payment_data: PaymentBase, db_session: Session = Depends(get_db)):
    db_payment = db_session.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")

    if payment_data.amount is not None:
        db_payment.amount = payment_data.amount
    if payment_data.payment_date is not None:
        db_payment.payment_date = payment_data.payment_date
    if payment_data.profit_loss is not None:
        db_payment.profit_loss = payment_data.profit_loss
    if payment_data.user_id is not None:
        db_payment.user_id = payment_data.user_id
    if payment_data.customer_id is not None:
        db_payment.customer_id = payment_data.customer_id

    db_session.commit()
    db_session.refresh(db_payment)
    return db_payment


@app.delete("/payments/{payment_id}", response_model=Payment)
def delete_payment(payment_id: int, db_session: Session = Depends(get_db)):
    db_payment = db_session.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if db_payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")

    db_session.delete(db_payment)
    db_session.commit()
    return db_payment


if __name__ == "__main__":
    models.Base.metadata.create_all(bind=engine)
    uvicorn.run(app, host="0.0.0.0", port=8000)
