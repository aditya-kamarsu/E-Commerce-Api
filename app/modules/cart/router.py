from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.cart.dependencies import get_cart_service

from app.modules.cart.schemas import AddToCartRequestSchema, CartResponseSchema,UpdateCartItemRequestSchema
from app.modules.cart.service import CartService

from app.modules.user.models import User

cart_router = APIRouter(
    prefix="/cart",
    tags=["Cart"],
)




@cart_router.post(
    "/items",
    response_model=CartResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def add_to_cart(
    request: AddToCartRequestSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    cart_service: CartService = Depends(get_cart_service),
):
    return cart_service.add_to_cart(
        db=db,
        request=request,
        current_user=current_user,
    )


@cart_router.get(
    "/",
    response_model=CartResponseSchema,
    status_code=status.HTTP_200_OK,
)
def get_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    cart_service: CartService = Depends(get_cart_service)
):
    return cart_service.get_cart(
        db=db,
        current_user=current_user,
    )


@cart_router.patch(
    "/items/{cart_item_id}",
    response_model=CartResponseSchema,
    status_code=status.HTTP_200_OK,
)
def update_cart_item(
    cart_item_id: int,
    request: UpdateCartItemRequestSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    cart_service: CartService = Depends(get_cart_service)
):
    return cart_service.update_quantity(
        db=db,
        cart_item_id=cart_item_id,
        request=request,
        current_user=current_user,
    )

@cart_router.delete(
    "/items/{cart_item_id}",
    response_model=CartResponseSchema,
    status_code=status.HTTP_200_OK,
)
def remove_cart_item(
    cart_item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    cart_service: CartService = Depends(get_cart_service)
):
    return cart_service.remove_item(
        db=db,
        cart_item_id=cart_item_id,
        current_user=current_user,
    )


@cart_router.delete(
    "/",
    response_model=CartResponseSchema,
    status_code=status.HTTP_200_OK,
)
def clear_cart(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    cart_service: CartService = Depends(get_cart_service)
):
    return cart_service.clear_cart(
        db=db,
        current_user=current_user,
    )


