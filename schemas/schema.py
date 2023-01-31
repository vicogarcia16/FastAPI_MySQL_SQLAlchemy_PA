from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    id: Optional[int]
    product: str
    price: float

class ProductAdd(BaseModel):
    product: str
    price: float
    
    class Config:
        orm_mode = True
    
class ProductUpdate(BaseModel):
    product: str
    price: float
    
    class Config:
        orm_mode = True
    
    