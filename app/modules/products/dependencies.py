from app.modules.categories.dependencies import get_category_repository
from app.modules.categories.repository import CategoryRepository
from app.modules.products.repository import ProductRepository
from app.modules.products.service import ProductService
from fastapi import Depends

def get_product_repository() -> ProductRepository:
    return ProductRepository()

def get_product_service(
        product_repository: ProductRepository = Depends(get_product_repository),
        category_repository: CategoryRepository = Depends(get_category_repository)
        ) -> ProductService:
    return ProductService(product_repository, category_repository)