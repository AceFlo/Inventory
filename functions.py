from sqlalchemy.exc import NoResultFound
from models import Product, Sale, Invoice, RemainingStock, SaleItem, StockIn, User, Customer, Payment


def create_user(db_session, user_data):
    user = User(**user_data.dict())
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


def update_user(db_session, user_id, user_data):
    user = db_session.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")

    if user_data.username is not None:
        user.username = user_data.username
    if user_data.email is not None:
        user.email = user_data.email
    if user_data.password is not None:
        user.password = user_data.password

    db_session.commit()
    db_session.refresh(user)
    return user


def create_product(db_session, product_data):
    product = Product(**product_data.dict())
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)
    return product


def update_product(db_session, product_id, product_data):
    product = db_session.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise ValueError("Product not found")

    if product_data.product_name is not None:
        product.product_name = product_data.product_name
    if product_data.price is not None:
        product.price = product_data.price
    if product_data.description is not None:
        product.description = product_data.description

    db_session.commit()
    db_session.refresh(product)
    return product


def delete_product(db_session, product_id):
    product = db_session.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise ValueError("Product not found")

    db_session.delete(product)
    db_session.commit()
    return product


def create_customer(db_session, customer_data):
    customer = Customer(**customer_data.dict())
    db_session.add(customer)
    db_session.commit()
    db_session.refresh(customer)
    return customer


def update_customer(db_session, customer_id, customer_data):
    customer = db_session.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise ValueError("Customer not found")

    if customer_data.name is not None:
        customer.name = customer_data.name
    if customer_data.address is not None:
        customer.address = customer_data.address
    if customer_data.phone is not None:
        customer.phone = customer_data.phone

    db_session.commit()
    db_session.refresh(customer)
    return customer


def delete_customer(db_session, customer_id):
    customer = db_session.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise ValueError("Customer not found")

    db_session.delete(customer)
    db_session.commit()
    return customer


def read_product(db_session, product_id):
    try:
        return db_session.query(Product).filter(Product.id == product_id).one()
    except NoResultFound:
        raise ValueError("Product not found")


def read_customer(db_session, customer_id):
    try:
        return db_session.query(Customer).filter(Customer.id == customer_id).one()
    except NoResultFound:
        raise ValueError("Customer not found")


def read_stock_in(db_session, stock_in_id):
    try:
        return db_session.query(StockIn).filter(StockIn.id == stock_in_id).one()
    except NoResultFound:
        raise ValueError("Stock-in entry not found")


def read_remaining_stock(db_session, stock_id):
    try:
        return db_session.query(RemainingStock).filter(RemainingStock.id == stock_id).one()
    except NoResultFound:
        raise ValueError("Remaining stock entry not found")


def read_invoice(db_session, invoice_id):
    try:
        return db_session.query(Invoice).filter(Invoice.id == invoice_id).one()
    except NoResultFound:
        raise ValueError("Invoice not found")


def read_payment(db_session, payment_id):
    try:
        return db_session.query(Payment).filter(Payment.id == payment_id).one()
    except NoResultFound:
        raise ValueError("Payment not found")


def calculate_total_amount(db_session, items):
    total_amount = 0
    for item in items:
        product = db_session.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise ValueError(f"Product with ID {item.product_id} not found")
        total_amount += product.price * item.quantity
    return total_amount


def validate_stock(db_session, items):
    for item in items:
        remaining_stock = db_session.query(RemainingStock).filter(RemainingStock.product_id == item.product_id).first()
        if not remaining_stock or remaining_stock.quantity < item.quantity:
            raise ValueError(f"Insufficient stock for Product ID {item.product_id}")


def update_stock(db_session, items):
    for item in items:
        remaining_stock = db_session.query(RemainingStock).filter(RemainingStock.product_id == item.product_id).first()
        if remaining_stock:
            remaining_stock.quantity -= item.quantity
            if remaining_stock.quantity < 0:
                raise ValueError(f"Stock cannot be negative for Product ID {item.product_id}")
    db_session.commit()


def create_sale(db_session, sale_data):
    total_amount = calculate_total_amount(db_session, sale_data.items)
    validate_stock(db_session, sale_data.items)

    sale = Sale(date=sale_data.date, total_amount=total_amount)
    db_session.add(sale)
    db_session.commit()

    for item in sale_data.items:
        sale_item = SaleItem(sale_id=sale.id, product_id=item.product_id, quantity=item.quantity)
        db_session.add(sale_item)

    update_stock(db_session, sale_data.items)

    invoice = Invoice(sale_id=sale.id, amount=total_amount, date=sale_data.date)
    db_session.add(invoice)
    db_session.commit()

    return sale, invoice


def create_stock_in(db_session, stock_in_data):
    stock_in = StockIn(**stock_in_data.dict())
    db_session.add(stock_in)
    db_session.commit()

    remaining_stock = db_session.query(RemainingStock).filter(RemainingStock.product_id == stock_in.product_id).first()
    if remaining_stock:
        remaining_stock.quantity += stock_in.quantity
    else:
        new_stock = RemainingStock(product_id=stock_in.product_id, quantity=stock_in.quantity)
        db_session.add(new_stock)

    db_session.commit()
    return stock_in
