

from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.core.authorization import require_role
from app.core.dependencies import get_db
from app.core.enums import UserRole
from app.modules.products.dependencies import get_product_service
from app.modules.products.repository import ProductRepository
from app.modules.products.schemas import ProductQueryParams, ProductResponse, UpdateProduct,CreateProduct
from app.modules.products.service import ProductService
from app.modules.auth.dependencies import get_current_user
from app.modules.user.models import User


product_router = APIRouter(
    prefix="/products",
    tags=["Products"]
    )





    
@product_router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    product_data: CreateProduct,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.SELLER, UserRole.ADMIN)
    ),
    product_service: ProductService = Depends(get_product_service),
):
    
    return product_service.create_product_service(
        db,
        product_data,
        current_user,
    )




@product_router.get("/", response_model=list[ProductResponse], status_code=status.HTTP_200_OK)
def get_all_products(
    query:Annotated[ProductQueryParams, Query()],
    db: Session = Depends(get_db),
    product_service: ProductService = Depends(get_product_service)
    
):
    return product_service.get_products_service(db, query)
    
    

@product_router.get("/{product_id}", 
                    response_model=ProductResponse, 
                    status_code=status.HTTP_200_OK)
def get_product_by_id(
    product_id: int,
    db: Session = Depends(get_db),
    product_service: ProductService = Depends(get_product_service)
):
    # Implementation for fetching a product by ID
    return product_service.get_product_by_id_service(db, product_id)


@product_router.patch("/{product_id}", 
                      response_model=ProductResponse,
                        status_code=status.HTTP_200_OK)
def update_product(product_id: int,
                   product_update: UpdateProduct,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(
                        require_role(UserRole.ADMIN, UserRole.SELLER)
                    ),
                    product_service: ProductService = Depends(get_product_service)
                    ):
    return product_service.update_product_service(db,
                                   product_id, 
                                   product_update, 
                                   current_user
                                   )


@product_router.delete("/{product_id}",status_code=status.HTTP_200_OK)
def delete_product(
    product_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(
        require_role(UserRole.ADMIN, UserRole.SELLER)
    ),
    product_service: ProductService = Depends(get_product_service)
    ):
    return product_service.delete_product_service(db, product_id, current_user)