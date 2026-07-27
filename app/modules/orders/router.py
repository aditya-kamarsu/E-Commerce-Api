
from app.core.dependencies import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.orders.schemas import OrderResponse
from app.modules.orders.service import OrderService
from app.modules.user.models import User
from fastapi import APIRouter, Depends
from app.modules.user.models import User
from app.modules.orders.dependencies import get_order_service
from app.modules.orders.schemas import OrderResponse

order_Routes = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@order_Routes.post("/",response_model=OrderResponse)
async def create_order(db = Depends(get_db),
                        user: User = Depends(get_current_user), 
                        order_service: OrderService = Depends(get_order_service)
                        ):
    order = order_service.create_order(db, user.id)
    return order



@order_Routes.get("/",response_model=list[OrderResponse])
async def get_orders(db = Depends(get_db),
                      user: User = Depends(get_current_user),
                      order_service: OrderService = Depends(get_order_service)):
    orders = order_service.user_order_service(db, user)
    return orders



@order_Routes.get("/{order_id}",response_model=OrderResponse)
async def get_order(order_id: int,
                    db = Depends(get_db), 
                    user: User = Depends(get_current_user), 
                    order_service: OrderService = Depends(get_order_service)
                    ):
    order = order_service.get_order(db, order_id, user)
    return order



@order_Routes.patch("/{order_id}/cancel",response_model=OrderResponse)
async def cancel_order( order_id: int, 
                        db = Depends(get_db), 
                        user: User = Depends(get_current_user), 
                        order_service: OrderService = Depends(get_order_service)):
    order = order_service.cancel_order_service(db, order_id,user)
    return order





