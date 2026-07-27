from app.modules.products.repository import ProductRepository
from app.modules.products.service import ProductService
from fastapi import Depends

def get_product_repository() -> ProductRepository:
    return ProductRepository()

def get_product_service(
        product_repository: ProductRepository = Depends(get_product_repository)
        ) -> ProductService:
    return ProductService(product_repository)