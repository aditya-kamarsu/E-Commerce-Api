
from fastapi import APIRouter




user_router = APIRouter()



@user_router.get("/me")
async def auth_get_profile():
    pass

@user_router.put("/me")
async def auth_update_profile():
    pass

@user_router.delete("/me")
async def auth_change_password():
    pass



