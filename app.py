from fastapi import Depends, FastAPI,HTTPException
from fastapi.responses import JSONResponse
from config.db import SessionLocal
from schemas import schema
from sqlalchemy.orm import Session
from routes.products import (create_product_sp, 
                             get_product_sp, 
                             get_products_sp,
                             update_product_sp,
                             delete_product_sp)

#model.Base.metadata.create_all(bind=engine)

app=FastAPI(
    title = "Inventario",
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
        
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )
        
@app.post("/products/", tags=["Productos"])
def create_product(product: schema.ProductAdd, db: Session = Depends(get_db)):
    product_data = product.model_dump()
    try:    
        created_product_id = create_product_sp(product_data["product"], product_data["price"], db)
        return {"message": "Product created","product_id": created_product_id}
    except:
        raise HTTPException(status_code=400, detail="Error creating product")


@app.get("/products/{product_id}/", response_model=schema.Product, tags=["Productos"])
def get_product(product_id: int, db: Session = Depends(get_db)):
    if product_id <= 0:
        raise HTTPException(status_code=404, detail="Product not found")
    try:
        product = get_product_sp(product_id, db)
        product_dict = dict(zip(product._fields, product))
        return schema.Product(**product_dict)
    except Exception as e:
        if str(e) == "Product not found":
            raise HTTPException(status_code=404, detail="Product not found")
        else:
            raise HTTPException(status_code=400, detail=f"Error retrieving product: {e}")
    
    
@app.get("/products/", tags=["Productos"])
def get_products(db: Session = Depends(get_db)):
    products = get_products_sp(db)
    if products is None:
        raise HTTPException(status_code=404, detail="Products not found")
    try:
        return {"Products":[schema.Product(**product) for product in products]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error retrieving products: {e}")


@app.put("/products/{product_id}/", response_model=schema.ProductUpdate, tags=["Productos"])
def update_product(product_id: int, update_p: schema.ProductUpdate, db: Session = Depends(get_db)):   
    
    try:
        get_product_sp(product_id, db)
        product = update_product_sp(product_id, update_p.product, update_p.price,db)
        product_dict = dict(zip(product._fields, product))
        return schema.ProductUpdate(**product_dict)
    except Exception as e:
        if str(e) == "Product not found":
            raise HTTPException(status_code=404, detail="Product not found")
        else:
            raise HTTPException(status_code=400, detail=f"Error updating product: {e}")


@app.delete("/products/{product_id}/", tags=["Productos"])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    if product_id <= 0:
        raise HTTPException(status_code=404, detail="Product not found")
    
    try:
        get_product_sp(product_id, db)
        deleted = delete_product_sp(product_id, db)
        if deleted:
            return {"message": "Product successfully deleted"}
    except Exception as e:
        if str(e) == "Product not found":
            raise HTTPException(status_code=404, detail="Product not found")
        raise HTTPException(status_code=400, detail=f"Error deleting product: {e}")