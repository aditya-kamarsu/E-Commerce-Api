
from itertools import product

from sqlalchemy.orm import Session
from app.core.enums import UserRole
from app.core.exceptions import DuplicateProductException, InvalidProductPriceException, InvalidProductStockException, ProductNotFoundException,PermissionDeniedException
from app.modules.categories.exceptions import CategoryNotFoundException
from app.modules.products.models import Product
from app.modules.products.repository import ProductRepository
from app.modules.products.schemas import CreateProduct, ProductQueryParams, UpdateProduct
from app.modules.user.models import User
from fastapi import HTTPException


class ProductService:
    def __init__(self, product_repository: ProductRepository,category_repository):
        self.product_repository = product_repository
        self.category_repository = category_repository




    def create_product_service(self,db:Session,product_data: CreateProduct,current_user: User):
        if (current_user.role != UserRole.SELLER and Product.seller_id != current_user.id):
                    raise HTTPException(
                        status_code=403,
                        detail="You are not authorized to modify this product."
                        )
        if product_data.price <= 0:
            raise InvalidProductPriceException(product_data.price)
        if product_data.stock < 0:
            raise InvalidProductStockException(product_data.stock)
        if self.product_repository.get_by_seller_and_name(db, current_user.id, product_data.name):
            raise HTTPException(status_code=400, detail="Product with the same name already exists for this seller.")


        category = self.category_repository.get_by_id(
            db,
            product_data.category_id
            )

        if not category:
            raise CategoryNotFoundException(product_data.category_id)
        
        product = Product(
            **product_data.model_dump(),
            seller_id=current_user.id)
        return self.product_repository.create_product(db, product)


    def get_product_by_id_service(self, db: Session, product_id: int):
        product = self.product_repository.get_product_by_id(db, product_id)
        if not product:
            raise ProductNotFoundException(product_id)
        return product  
        

    def get_products_service(self, db: Session, query: ProductQueryParams):
        return self.product_repository.get_all_products(db, query)


    

    def update_product_service(self,db: Session,product_id: int,product_update: UpdateProduct,current_user: User,):


        if (current_user.role != UserRole.SELLER and product.seller_id != current_user.id):
            raise HTTPException(
                status_code=403,
                detail="You are not authorized to modify this product."
                )
        # Check if product exists
        product = self.product_repository.get_product_by_id(db,product_id)

        if not product:
            raise ProductNotFoundException(product_id)

        if product_update.category_id is not None:
            category = self.category_repository.get_by_id(
                db,
                product_update.category_id
                )
            if not category:
                raise CategoryNotFoundException(product_update.category_id)
        

        # Check ownership
        if product.seller_id != current_user.id:
            raise PermissionDeniedException()



       
        # Validate price
        if (
            product_update.price is not None
            and product_update.price <= 0
        ):
            raise InvalidProductPriceException(product_update.price)

        # Validate stock
        if (
            product_update.stock is not None
            and product_update.stock < 0
        ):
            raise InvalidProductStockException(product_update.stock)

        # Check duplicate product name
        if product_update.name is not None:
            existing_product = self.product_repository.get_by_seller_and_name(
                db,
                current_user.id,
                product_update.name,
            )

            if (
                existing_product
                and existing_product.id != product.id
            ):
                raise DuplicateProductException(product_update.name)

        # Update only the provided fields
        for key, value in product_update.model_dump(
            exclude_unset=True
        ).items():
            setattr(product, key, value)

        # Save changes
        return self.product_repository.update_product(
            db,
            product
        )

    def delete_product_service(
            self,
            db: Session,
            product_id: int, 
            current_user: User
            ):
        if (current_user.role != UserRole.SELLER and product.seller_id != current_user.id):
                    raise HTTPException(
                        status_code=403,
                        detail="You are not authorized to modify this product."
                        )
         
        product = self.product_repository.get_product_by_id(db, product_id)
        if not product:
            raise ProductNotFoundException(product_id)

        if product.seller_id != current_user.id:
            raise PermissionDeniedException()
    
        self.product_repository.delete_product(db, product_id)
        return {"message": "Product deleted successfully."}


