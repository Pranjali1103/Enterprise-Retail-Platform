from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.db import get_db

from models.product import Product
from models.customer import Customer
from models.store import Store
from models.sale import Sale
from models.inventory import Inventory

app = FastAPI(
    title="Enterprise Retail Analytics Platform",
    version="1.0.0"
)

# =====================================================
# PRODUCTS
# =====================================================

@app.get("/api/products")
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@app.get("/api/products/{product_id}")
def get_product(
    product_id: str,
    db: Session = Depends(get_db)
):
    product = (
        db.query(Product)
        .filter(Product.product_id == product_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


@app.post(
    "/api/products",
    status_code=status.HTTP_201_CREATED
)
def create_product(
    product_id: str,
    product_name: str,
    category: str,
    brand: str,
    unit_price: float,
    supplier_id: str,
    status_value: str,
    db: Session = Depends(get_db)
):

    existing = (
        db.query(Product)
        .filter(Product.product_id == product_id)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=409,
            detail="Product already exists"
        )

    product = Product(
        product_id=product_id,
        product_name=product_name,
        category=category,
        brand=brand,
        unit_price=unit_price,
        supplier_id=supplier_id,
        status=status_value
    )

    db.add(product)
    db.commit()

    return {"message": "Product created"}


@app.put("/api/products/{product_id}")
def update_product(
    product_id: str,
    product_name: str,
    db: Session = Depends(get_db)
):

    product = (
        db.query(Product)
        .filter(Product.product_id == product_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    product.product_name = product_name

    db.commit()

    return {"message": "Product updated"}


@app.delete("/api/products/{product_id}")
def deactivate_product(
    product_id: str,
    db: Session = Depends(get_db)
):

    product = (
        db.query(Product)
        .filter(Product.product_id == product_id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    product.status = "Inactive"

    db.commit()

    return {"message": "Product deactivated"}


# =====================================================
# CUSTOMERS
# =====================================================

@app.get("/api/customers")
def get_customers(db: Session = Depends(get_db)):
    return db.query(Customer).all()


@app.get("/api/customers/{customer_id}")
def get_customer(
    customer_id: str,
    db: Session = Depends(get_db)
):

    customer = (
        db.query(Customer)
        .filter(Customer.customer_id == customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer


@app.post("/api/customers")
def create_customer(
    customer_id: str,
    customer_name: str,
    email: str,
    mobile: str,
    city: str,
    customer_type: str,
    db: Session = Depends(get_db)
):

    customer = Customer(
        customer_id=customer_id,
        customer_name=customer_name,
        email=email,
        mobile=mobile,
        city=city,
        customer_type=customer_type
    )

    db.add(customer)
    db.commit()

    return {"message": "Customer created"}


@app.put("/api/customers/{customer_id}")
def update_customer(
    customer_id: str,
    customer_name: str,
    db: Session = Depends(get_db)
):

    customer = (
        db.query(Customer)
        .filter(Customer.customer_id == customer_id)
        .first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    customer.customer_name = customer_name

    db.commit()

    return {"message": "Customer updated"}


# =====================================================
# STORES
# =====================================================

@app.get("/api/stores")
def get_stores(db: Session = Depends(get_db)):
    return db.query(Store).all()


@app.get("/api/stores/{store_id}")
def get_store(
    store_id: str,
    db: Session = Depends(get_db)
):

    store = (
        db.query(Store)
        .filter(Store.store_id == store_id)
        .first()
    )

    if not store:
        raise HTTPException(
            status_code=404,
            detail="Store not found"
        )

    return store


@app.post("/api/stores")
def create_store(
    store_id: str,
    store_name: str,
    city: str,
    state: str,
    store_manager: str,
    status_value: str,
    db: Session = Depends(get_db)
):

    store = Store(
        store_id=store_id,
        store_name=store_name,
        city=city,
        state=state,
        store_manager=store_manager,
        status=status_value
    )

    db.add(store)
    db.commit()

    return {"message": "Store created"}


@app.put("/api/stores/{store_id}")
def update_store(
    store_id: str,
    store_name: str,
    db: Session = Depends(get_db)
):

    store = (
        db.query(Store)
        .filter(Store.store_id == store_id)
        .first()
    )

    if not store:
        raise HTTPException(
            status_code=404,
            detail="Store not found"
        )

    store.store_name = store_name

    db.commit()

    return {"message": "Store updated"}


# =====================================================
# SALES
# =====================================================

@app.get("/api/sales")
def get_sales(db: Session = Depends(get_db)):
    return db.query(Sale).all()


@app.get("/api/sales/{sale_id}")
def get_sale(
    sale_id: str,
    db: Session = Depends(get_db)
):

    sale = (
        db.query(Sale)
        .filter(Sale.sale_id == sale_id)
        .first()
    )

    if not sale:
        raise HTTPException(
            status_code=404,
            detail="Sale not found"
        )

    return sale


@app.get("/api/sales/store/{store_id}")
def get_sales_by_store(
    store_id: str,
    db: Session = Depends(get_db)
):

    return (
        db.query(Sale)
        .filter(Sale.store_id == store_id)
        .all()
    )


@app.get("/api/sales/product/{product_id}")
def get_sales_by_product(
    product_id: str,
    db: Session = Depends(get_db)
):

    return (
        db.query(Sale)
        .filter(Sale.product_id == product_id)
        .all()
    )


@app.get("/api/sales/date/{sale_date}")
def get_sales_by_date(
    sale_date: str,
    db: Session = Depends(get_db)
):

    return (
        db.query(Sale)
        .filter(Sale.sale_date == sale_date)
        .all()
    )


# =====================================================
# INVENTORY
# =====================================================

@app.get("/api/inventory")
def get_inventory(db: Session = Depends(get_db)):
    return db.query(Inventory).all()


@app.get("/api/inventory/store/{store_id}")
def inventory_by_store(
    store_id: str,
    db: Session = Depends(get_db)
):

    return (
        db.query(Inventory)
        .filter(
            Inventory.store_id == store_id
        )
        .all()
    )


@app.get("/api/inventory/low-stock")
def low_stock(
    db: Session = Depends(get_db)
):

    return (
        db.query(Inventory)
        .filter(
            Inventory.available_quantity
            <= Inventory.reorder_level
        )
        .all()
    )