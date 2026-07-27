from fastapi import Depends
from app.modules.cart.repository import CartRepository, CartItemRepository
from app.modules.orders.service import OrderService
from app.modules.products.repository import ProductRepository
from app.modules.orders.repository import OrderRepository, OrderItemRepository
from app.modules.cart.dependencies import get_cart_repository, get_cart_item_repository
from app.modules.products.dependencies import get_product_repository

def get_order_repository() -> OrderRepository:
    return OrderRepository()

def get_order_item_repository() -> OrderItemRepository:
    return OrderItemRepository()

def get_order_service(
        cart_repository: CartRepository = Depends(get_cart_repository),
        product_repository: ProductRepository = Depends(get_product_repository),
        order_repository: OrderRepository = Depends(get_order_repository),
        order_item_repository: OrderItemRepository = Depends(get_order_item_repository),
        cart_item_repository: CartItemRepository = Depends(get_cart_item_repository)
):
   
    return OrderService(
        cartRepository=cart_repository,
        productRepository=product_repository,
        orderRepository=order_repository,
        orderItemRepository=order_item_repository,
        cartItemRepository=cart_item_repository
    )

    
