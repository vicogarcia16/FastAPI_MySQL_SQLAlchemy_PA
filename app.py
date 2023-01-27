from fastapi import Depends, FastAPI,HTTPException
from config.db import SessionLocal, engine
from models import model
from schemas import schema
from sqlalchemy.orm import Session
from routes.products import create_product_sp

#model.Base.metadata.create_all(bind=engine)

app=FastAPI(
    title = "Productos",
    description = "CRUD en FastAPI",

    docs_url='/',
    redoc_url='/redoc' 
    )   

# Dependencia
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.post("/products/")
def create_product(product: schema.Products, db: Session = Depends(get_db)):
    try:
        product_data = product.dict()
        created_product_id = create_product_sp(product_data["product"], product_data["price"], db)
        return {"message": "Product created","product_id": created_product_id}
    except:
        raise HTTPException(status_code=400, detail="Error creating product")


