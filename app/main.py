from fastapi import FastAPI
from app.core.database import engine
from app.core.database import Base
from app.modules.user.router import user_router
from app.modules.auth.routes import auth_router
from app.modules.products.router import product_router
from app.modules.cart.router import cart_router
from app.modules.orders.router import order_Routes



app = FastAPI()

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(product_router)  
app.include_router(cart_router)     
app.include_router(order_Routes)



