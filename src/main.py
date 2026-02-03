import src.models


from src.routers.item_router import router as item_router
from src.routers.price_router import router as price_router
from src.routers.stock_router import router as stock_router
from src.routers.stock_line_router import router as stock_line_router
from src.routers.update_item_router import router as update_item_router
from src.routers.update_router import router as update_router
from src.routers.shop_router import router as shop_router
from src.routers import order_item_router
from src.routers import conditionnement_item_router


# from src.routers.users_router import users as users_router
# Application principale FastAPI pour DigiCheese API
from src.config.open_api import openapi_config
from fastapi import FastAPI, Request
from src.security import jwt_validation_middleware
from src.routers import api_router

# Création de l'application FastAPI
app = FastAPI(title="DigiCheese API")

app.openapi = lambda: openapi_config(app)

app.include_router(api_router)
app.include_router(item_router)
app.include_router(price_router)
app.include_router(stock_router)
app.include_router(stock_line_router)
app.include_router(update_item_router)
app.include_router(update_router)
app.include_router(shop_router)
app.include_router(order_item_router)
app.include_router(conditionnement_item_router)
app.middleware("http")(jwt_validation_middleware)

# Endpoint de santé pour vérifier que l'API fonctionne
@app.get("/health")
async def health_check():
    return {"status": "ok"}
