


from fastapi import Depends

from app.modules.products.dependencies import get_product_repository
from app.modules.products.repository import ProductRepository
from app.modules.wishlist.repository import WishlistRepository
from app.modules.wishlist.services import WishlistService

    
def get_wishlist_repository() -> WishlistRepository:
    return WishlistRepository()

    


def get_wishlist_service(
    wishlist_repository: WishlistRepository = Depends(
        get_wishlist_repository
    ),
    product_repository: ProductRepository = Depends(
        get_product_repository
    ),
) -> WishlistService:

    return WishlistService(
        wishlist_repository=wishlist_repository,
        product_repository=product_repository,
    )