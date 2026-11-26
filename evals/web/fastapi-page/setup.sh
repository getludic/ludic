#!/usr/bin/env bash
# Workspace: an existing FastAPI app with a JSON API.
set -euo pipefail

cat > pyproject.toml <<'EOF'
[project]
name = "acme-shop"
version = "0.1.0"
requires-python = ">=3.14"
dependencies = ["fastapi>=0.115", "ludic[fastapi,full]>=1.1.2,<2"]
EOF

cat > main.py <<'EOF'
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    price: float


PRODUCTS = [
    Product(id=1, name="Teapot", price=24.5),
    Product(id=2, name="Mug", price=8.0),
    Product(id=3, name="Kettle", price=39.9),
]

app = FastAPI()


@app.get("/api/products")
def list_products() -> list[Product]:
    return PRODUCTS


@app.get("/api/products/{product_id}")
def get_product(product_id: int) -> Product:
    for product in PRODUCTS:
        if product.id == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")
EOF
