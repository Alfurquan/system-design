from fastapi import APIRouter
from typing import List
from models.response_models import ProductResponse, CategoryResponse
import json
import os

router = APIRouter()

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data"))
PRODUCTS_PATH = os.path.join(DATA_DIR, "products.json")
CATEGORIES_PATH = os.path.join(DATA_DIR, "categories.json")

@router.get("/")
async def get_products(response_model=List[ProductResponse]):
    with open(PRODUCTS_PATH, 'r') as f:
        raw_products = json.load(f)
    with open(CATEGORIES_PATH, 'r') as f:
        raw_categories = json.load(f)

    category_map = {cat["id"]: CategoryResponse(**cat) for cat in raw_categories}

    product_responses = []
    for product in raw_products:
        category = category_map.get(product["category_id"])
        if category:
            product_resp = ProductResponse(
                id=product["id"],
                name=product["name"],
                price=product["price"],
                category=category,
                seller_id=product["seller_id"]
            )
            product_responses.append(product_resp)

    return product_responses
