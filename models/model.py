from sqlalchemy import Integer, Column, Float, String
from config.db import Base

class Products(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    product = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)