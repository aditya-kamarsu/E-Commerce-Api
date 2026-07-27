from fastapi import Depends
from app.modules.cart.repository import CartItemRepository, CartRepository
from app.modules.cart.service import CartService
from app.modules.products.dependencies import get_product_repository
from app.modules.products.repository import ProductRepository



def get_cart_repository()->CartRepository:
    return CartRepository()

def get_cart_item_repository()->CartItemRepository:
    return CartItemRepository()

def get_cart_service(
        cart_repository: CartRepository = Depends(get_cart_repository),
        cart_item_repository: CartItemRepository = Depends(get_cart_item_repository),
        product_repository: ProductRepository = Depends(get_product_repository)
        )->CartService:
    return CartService(cart_repository, cart_item_repository, product_repository)