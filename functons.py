from sqlalchemy.orm import Session
from datetime import datetime
import models
from schemas import StockInBase, InvoiceBase, PaymentBase, RemainingStockBase


def calculate_gst_and_discount(total_amount):
    discount_rate = 0.10  # 10% discount
    gst_rate = 0.18  # 18% GST

    discount = total_amount * discount_rate
    taxable_amount = total_amount - discount
    gst = taxable_amount * gst_rate
    final_amount = taxable_amount + gst

    return discount, gst, final_amount


def create_stock_in(db: Session, stock_in: StockInBase):
    db_stock_in = models.StockIn(**stock_in.dict())
    db.add(db_stock_in)

    product = db.query(models.Product).filter(models.Product.id == stock_in.product_id).first()
    if not product:
        raise ValueError("Product not found")

    total_amount = product.price * stock_in.quantity

    discount, gst, final_amount = calculate_gst_and_discount(total_amount)

    invoice = models.Invoice(
        invoice_date=datetime.now(),
        total_amount=final_amount,
        gst=gst,
        discount=discount,
        user_id=stock_in.user_id,
        customer_id=stock_in.customer_id
    )
    db.add(invoice)

    payment = models.Payment(
        amount=final_amount,
        payment_date=datetime.now(),
        profit_loss=final_amount - total_amount,
        user_id=stock_in.user_id,
        customer_id=stock_in.customer_id
    )
    db.add(payment)

    db.commit()
    db.refresh(db_stock_in)
    db.refresh(invoice)
    db.refresh(payment)
    return db_stock_in


def create_invoice(db: Session, invoice_data: InvoiceBase):
    db_invoice = models.Invoice(**invoice_data.dict())
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice


def read_invoice(db: Session, invoice_id: int):
    db_invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if db_invoice is None:
        raise ValueError("Invoice not found")
    return db_invoice


def update_invoice(db: Session, invoice_id: int, invoice_data: InvoiceBase):
    db_invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if db_invoice is None:
        raise ValueError("Invoice not found")

    if invoice_data.invoice_date is not None:
        db_invoice.invoice_date = invoice_data.invoice_date
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

    db.commit()
    db.refresh(db_invoice)
    return db_invoice


def delete_invoice(db: Session, invoice_id: int):
    db_invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if db_invoice is None:
        raise ValueError("Invoice not found")

    db.delete(db_invoice)
    db.commit()
    return db_invoice


def create_payment(db: Session, payment_data: PaymentBase):
    db_payment = models.Payment(**payment_data.dict())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment


def read_payment(db: Session, payment_id: int):
    db_payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if db_payment is None:
        raise ValueError("Payment not found")
    return db_payment


def update_payment(db: Session, payment_id: int, payment_data: PaymentBase):
    db_payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if db_payment is None:
        raise ValueError("Payment not found")

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

    db.commit()
    db.refresh(db_payment)
    return db_payment


def delete_payment(db: Session, payment_id: int):
    db_payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if db_payment is None:
        raise ValueError("Payment not found")

    db.delete(db_payment)
    db.commit()
    return db_payment


def create_remaining_stock(db: Session, remaining_stock_data: RemainingStockBase):
    db_remaining_stock = models.RemainingStock(**remaining_stock_data.dict())
    db.add(db_remaining_stock)
    db.commit()
    db.refresh(db_remaining_stock)
    return db_remaining_stock


def read_remaining_stock(db: Session, stock_id: int):
    db_remaining_stock = db.query(models.RemainingStock).filter(models.RemainingStock.id == stock_id).first()
    if db_remaining_stock is None:
        raise ValueError("Remaining Stock not found")
    return db_remaining_stock


def update_remaining_stock(db: Session, stock_id: int, remaining_stock_data: RemainingStockBase):
    db_remaining_stock = db.query(models.RemainingStock).filter(models.RemainingStock.id == stock_id).first()
    if db_remaining_stock is None:
        raise ValueError("Remaining Stock not found")

    if remaining_stock_data.product_id is not None:
        db_remaining_stock.product_id = remaining_stock_data.product_id
    if remaining_stock_data.quantity is not None:
        db_remaining_stock.quantity = remaining_stock_data.quantity

    db.commit()
    db.refresh(db_remaining_stock)
    return db_remaining_stock


def delete_remaining_stock(db: Session, stock_id: int):
    db_remaining_stock = db.query(models.RemainingStock).filter(models.RemainingStock.id == stock_id).first()
    if db_remaining_stock is None:
        raise ValueError("Remaining Stock not found")

    db.delete(db_remaining_stock)
    db.commit()
    return db_remaining_stock
