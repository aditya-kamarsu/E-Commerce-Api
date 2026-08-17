from decimal import Decimal

from sqlalchemy.orm import Session
from app.core.exceptions import ProductNotFoundException, InvalidQuantityException, ProductInactiveException, InsufficientStockException,  CartNotFoundException, CartItemNotFoundException
from app.modules.cart.models import Cart, CartItem
from app.modules.cart.schemas import AddToCartRequestSchema,UpdateCartItemRequestSchema, CartResponseSchema, CartItemResponseSchema
from app.modules.user.models import User


class CartService:
    def __init__(self,
                  cart_repository,
                  cart_item_repository,
                  product_repository
                ):
        self.cart_repository = cart_repository
        self.cart_item_repository = cart_item_repository
        self.product_repository = product_repository
        

    def add_to_cart(
        self,
        db: Session,
        current_user: User,
        request: AddToCartRequestSchema
    ) -> CartResponseSchema:

        # Validate quantity
        if request.quantity <= 0:
            raise InvalidQuantityException(
                "Quantity must be greater than zero."
            )

        # Get product
        product = self.product_repository.get_product_by_id(
            db,
            request.product_id
        )

        if not product:
            raise ProductNotFoundException(
                f"Product with ID {request.product_id} not found."
            )

        # Check product availability
        if not product.is_active:
            raise ProductInactiveException(
                f"Product with ID {request.product_id} is not available for purchase."
            )

        # Get user's cart
        cart = self.cart_repository.get_by_user_id(
            db,
            current_user.id
        )

        # Create cart if it doesn't exist
        if not cart:
            cart = Cart(user_id=current_user.id)
            cart = self.cart_repository.create_cart(
                db,
                cart
            )

        # Check if product already exists in cart
        cart_item = self.cart_item_repository.get_by_cart_and_product(
            db,
            cart.id,
            product.id
        )

        if cart_item:
            # Update existing cart item
            new_quantity = cart_item.quantity + request.quantity

            if new_quantity > product.stock:
                raise InsufficientStockException(
                    f"Only {product.stock} items available in stock."
                )

            cart_item.quantity = new_quantity

            cart_item = self.cart_item_repository.update_cart_item(
                db,
                cart_item
            )

        else:
            # Create new cart item
            if request.quantity > product.stock:
                raise InsufficientStockException(
                    f"Only {product.stock} items available in stock."
                )

            cart_item = CartItem(
                cart_id=cart.id,
                product_id=product.id,
                quantity=request.quantity
            )

            cart_item = self.cart_item_repository.create_cart_item(
                db,
                cart_item
            )

            if not cart_item:
                raise CartItemCreationException(
                    "Failed to add item to cart."
                )

        # TODO:
        # Build and return CartResponse
        return self._build_cart_response(db, cart)
    


    def get_cart(self, db:Session, current_user: User)->CartResponseSchema:
        # Logic to retrieve the user's cart
        cart = self.cart_repository.get_by_user_id(
            db,
            current_user.id
        )

        if not cart:
            return CartResponseSchema(items=[], total=Decimal("0.00"))
        return self._build_cart_response(db, cart)



    def update_quantity(self, db:Session, current_user: User, cart_item_id: int, request:UpdateCartItemRequestSchema)->CartResponseSchema:
        # Logic to update the quantity of an item in the user's cart
        if request.quantity <= 0:
            raise InvalidQuantityException(
                "Quantity must be greater than zero."
            )
        cart = self.cart_repository.get_by_user_id(
            db,
            current_user.id
        )

        if not cart:
            raise CartNotFoundException(
                "Cart not found for the user."
            )
        
        cart_item = self.cart_item_repository.get_cart_item_by_id(
            db,
            cart_item_id
        )
        
        if not cart_item:
            raise CartItemNotFoundException(
                "Cart item not found."
            )
        
        if cart_item.cart_id != cart.id:
            raise CartItemNotFoundException(
                "Cart item not found."
            )
        if request.quantity > cart_item.product.stock:
            raise InsufficientStockException(
                f"Only {cart_item.product.stock} items available in stock."
            )
        cart_item.quantity = request.quantity
        self.cart_item_repository.update_cart_item(
            db,
            cart_item
        )
        return self._build_cart_response(db, cart)



    def remove_item(self, db:Session, current_user: User, cart_item_id: int)->CartResponseSchema:
        # Logic to remove an item from the user's cart
        cart = self.cart_repository.get_by_user_id(
            db,
            current_user.id
        )
        if not cart:
            raise CartNotFoundException(
                "Cart not found for the user."
            )
        cart_item = self.cart_item_repository.get_cart_item_by_id(
            db,
            cart_item_id
        )

        if not cart_item:
            raise CartItemNotFoundException(
                "Cart item not found."
            )
        if cart_item.cart_id != cart.id:
            raise CartItemNotFoundException(
                "Cart item not found."
            )
        self.cart_item_repository.delete_cart_item(
            db,
            cart_item
        )
        return self._build_cart_response(db, cart)
    

        

    def clear_cart(self, db:Session, current_user: User) -> CartResponseSchema:
        # Logic to clear the user's cart
        cart = self.cart_repository.get_by_user_id(
            db,
            current_user.id
        )
        if not cart:
            return CartResponseSchema(items=[], total=Decimal("0.00"))
        
        self.cart_item_repository.delete_all_by_cart(
            db,
            cart.id
        )
        return CartResponseSchema(items=[], total=Decimal("0.00"))



    
    def _build_cart_response(self, db: Session, cart: Cart) -> CartResponseSchema:
        # Logic to build and return a CartResponse object
        items = self.cart_item_repository.get_all_by_cart(db, cart.id)

        response_items: list[CartItemResponseSchema] = []
        total = Decimal("0.00")
        for item in items:
            product = item.product  # Assuming a relationship exists between CartItem and Product
            if not product:
                raise ProductNotFoundException(
                    f"Product with ID {item.product_id} not found."
                )

            subtotal = product.price * item.quantity
            total += subtotal

            response_items.append(
                CartItemResponseSchema(
                    id=item.id,
                    product_id=product.id,
                    product_name=product.name,
                    price=product.price,
                    quantity=item.quantity,
                    subtotal=subtotal
                )
            )

        return CartResponseSchema(items=response_items, total=total)
    