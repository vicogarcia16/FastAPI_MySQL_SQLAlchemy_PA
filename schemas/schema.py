from pydantic import BaseModel

class Products(BaseModel):
    product: str
    price: float
    
    class Config:
        orm_mode = True