from fastapi import HTTPException
from http.client import HTTPException
from sqlalchemy import select
from app.modules.cart.repository import CartItemRepository, CartRepository
from app.modules.orders.models import Order, OrderItem
from app.modules.orders.repository import OrderItemRepository, OrderRepository
from app.modules.orders.utils import OrderStatus
from app.modules.products.repository import ProductRepository
from app.modules.user.utils import UserRole





class OrderService:

    def __init__(self, cartRepository: CartRepository,
                 cartItemRepository: CartItemRepository,
                 productRepository: ProductRepository, 
                 orderRepository: OrderRepository,
                 orderItemRepository: OrderItemRepository
                 ):
        self.cartRepository = cartRepository
        self.productRepository = productRepository
        self.orderRepository = orderRepository
        self.orderItemRepository = orderItemRepository
        self.cartItemRepository = cartItemRepository

    def create_order(self, db, user_id):
        try:
            cart,cart_items = self._validate_cart(db, user_id)

            products, total = self._calculate_total(db, cart_items)

            order = self.orderRepository.create_order(
                db,
                Order(
                    user_id=user_id,
                    total_amount=total,
                    shipping_fee=0,
                    tax_amount=0,
                    status=OrderStatus.PENDING,
                ),
            )

            self._create_order_items(db, order, cart_items, products)

            self._update_stock(db, cart_items, products)

            self.cartItemRepository.delete_all_by_cart(db, cart.id)

            db.commit()

            return order

        except Exception:
            db.rollback()
            raise
    
    









    def get_order(self, db, order_id: int, user):
        
        order = self.orderRepository.get_by_id(db, order_id)

        if not order:
            raise HTTPException(
                status_code=404,
                detail="Order not found."
            )

        if order.user_id != user.id and user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=403,
                detail="You are not authorized to access this order."
            )

        return order
    

        

    def user_order_service(self, db, user):
        orders = self.orderRepository.get_by_user(db, user.id)
        return orders




    def cancel_order_service(self,db, order_id: int, user):
        try:
            order = self._get_order_or_404(db, order_id)
            self._check_order_owner(order, user)
            self._validate_cancel_status(order)

            order_items=self.orderItemRepository.get_by_order(db, order.id)

            self._restore_stock(db, order_items)

            order.status = OrderStatus.CANCELLED
            self.orderRepository.update(db, order)

            db.commit()
            return order
        except Exception:
            db.rollback()
            raise
    

                






        # here are the helper function to the object 

    def _validate_cart(self, db, user_id):
        cart = self.cartRepository.get_by_user_id(db, user_id)

        if not cart:
            raise Exception("Cart not found for the user.")
        
        cart_items = self.cartItemRepository.get_all_by_cart(db, cart.id)

        if not cart_items:
            raise Exception("No items in the cart to create an order.")
        
        return cart, cart_items
    
    
    def _calculate_total(self, db, cart_items):
        products = {}
        total = 0

        for item in cart_items:
            product = self.productRepository.get_product_by_id(db, item.product_id)
            
            if not product:
                raise Exception(f"Product with ID {item.product_id} not found.")
            
            if product.stock < item.quantity:
                raise Exception(f"Insufficient stock for product {product.name}.")
            total += product.price * item.quantity
            products[item.product_id] = product
          

        return products, total

    def _create_order_items(self, db, order, cart_items, products):
        order_items = []

        for item in cart_items:
            product = products[item.product_id]
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price_at_purchase=product.price,
                subtotal=product.price * item.quantity
            )
            order_items.append(order_item)

        self.orderItemRepository.create_many(db, order_items)
        return order_items
        

    def _update_stock(self, db, cart_items, products):

        for item in cart_items:
            product = products[item.product_id]
            product.stock -= item.quantity
            self.productRepository.update_product(db, product)



    # here the helper funtion for the cancell order 

    def _get_order_or_404(self, db, order_id):
        order = self.orderRepository.get_by_id(db, order_id)
        if not order:
            raise HTTPException(
                status_code=404,
                detail="Order not found."
            )
        return order
    
    def _check_order_owner(self, order,user):
        if order.user_id != user.id and user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=403,
                detail="You are not authorized to cancel this order."
            )
        
    def _validate_cancel_status(self, order):
        if order.status == OrderStatus.CANCELLED:
            raise HTTPException(
                status_code=400,
                detail="Only pending orders can be cancelled."
            )
        
        if order.status in (
            OrderStatus.SHIPPED,
            OrderStatus.DELIVERED,
        ):
            raise HTTPException(
                status_code=400,
                detail="Shipped or delivered orders cannot be cancelled."
            )
        
    
    def _restore_stock(self, db, order_items):
        for item in order_items:
            product = self.productRepository.get_product_by_id(db, item.product_id)
            product.stock += item.quantity
            self.productRepository.update_product(db, product)

        






