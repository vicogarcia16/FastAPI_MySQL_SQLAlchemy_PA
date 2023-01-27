from sqlalchemy import text
from sqlalchemy.orm import Session

def create_product_sp(product: str, price: float, db: Session):
    stmt = text("CALL create_product(:product, :price)")
    result = db.execute(stmt, {"product": product, "price": price}).fetchone()
    db.commit()
    product_id = result[0]
    return product_id
    