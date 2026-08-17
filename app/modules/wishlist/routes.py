from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.user.models import User

from app.modules.wishlist.dependencies import get_wishlist_service
from app.modules.wishlist.schemas import WishlistResponse
from app.modules.wishlist.services import WishlistService


wishlist_router = APIRouter(
    prefix="/wishlist",
    tags=["Wishlist"],
)


@wishlist_router.post(
    "/items/{product_id}",
    status_code=status.HTTP_201_CREATED,
)
def add_to_wishlist(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    wishlist_service: WishlistService = Depends(
        get_wishlist_service
    ),
):
    return wishlist_service.add_to_wishlist(
        db=db,
        product_id=product_id,
        current_user=current_user,
    )


@wishlist_router.get(
    "/",
    response_model=WishlistResponse,
    status_code=status.HTTP_200_OK,
)
def get_wishlist(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    wishlist_service: WishlistService = Depends(
        get_wishlist_service
    ),
):
    items = wishlist_service.get_wishlist(
        db=db,
        current_user=current_user,
    )

    return {
        "items": items
    }


@wishlist_router.delete(
    "/items/{product_id}",
    status_code=status.HTTP_200_OK,
)
def remove_from_wishlist(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    wishlist_service: WishlistService = Depends(
        get_wishlist_service
    ),
):
    return wishlist_service.remove_from_wishlist(
        db=db,
        product_id=product_id,
        current_user=current_user,
    )


@wishlist_router.delete(
    "/",
    status_code=status.HTTP_200_OK,
)
def clear_wishlist(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    wishlist_service: WishlistService = Depends(
        get_wishlist_service
    ),
):
    return wishlist_service.clear_wishlist(
        db=db,
        current_user=current_user,
    )