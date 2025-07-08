from typing import List
from pydantic import BaseModel

class Product(BaseModel):
    id: str
    name: str
    price: float
    category_id: str
    seller_id: str
