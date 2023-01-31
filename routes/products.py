from sqlalchemy import text
from sqlalchemy.orm import Session

def create_product_sp(product: str, price: float, db: Session):
    stmt = text("CALL create_product(:product, :price)")
    result = db.execute(stmt, {"product": product, "price": price}).fetchone()
    db.commit()
    product_id = result[0]
    return product_id

def get_product_sp(product_id: int, db: Session):
    stmt = text("CALL get_product(:product_id)")
    result = db.execute(stmt, {"product_id": product_id}).fetchone()
    if result is None:
        raise Exception("Product not found")
    return result

def get_products_sp(db: Session):
    stmt = text("CALL get_products()")
    result = db.execute(stmt).fetchall()
    products = [{"id": r[0], "product": r[1], "price": r[2]} for r in result]
    db.commit()
    return products


def update_product_sp(product_id: int, product: str, price: float, db: Session):
    stmt = text("CALL update_product(:id, :product, :price)")
    result = db.execute(stmt, {"id": product_id, "product": product, "price": price})
    db.commit()
    return result.fetchone()


def delete_product_sp(product_id: int, db: Session):
    stmt = text("CALL delete_product(:product_id)")
    result = db.execute(stmt, {"product_id": product_id})
    db.commit()
    return result