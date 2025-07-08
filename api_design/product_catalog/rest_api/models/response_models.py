from pydantic import BaseModel
from typing import List

class CategoryResponse(BaseModel):
    id: str
    name: str

class ProductResponse(BaseModel):
    id: str
    name: str
    price: float
    category: CategoryResponse
