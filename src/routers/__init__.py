from fastapi import APIRouter

from .client_router import clients
from .department_router import departements
from .stock_router import router as stocks
from .commande_router import router as orders
from .user_router import users
from .auth_router import auth
from .admin_roles_router import router as admin_roles
from .commune_router import router as commune_router
from .commande_router import router as commande_router
from .conditionnement import router as conditionnement_router
# from .detail_commande import router as detail_commande_router
from .zip_code_router import zip_codes
from .order_item_router import router as order_item_router
from .conditionnement_item_router import router as conditionnement_item_router

api_router = APIRouter()

api_router.include_router(auth, prefix="/auth", tags=["Auth"])
api_router.include_router(users, prefix="/users", tags=["Admin: Users"])
api_router.include_router(admin_roles, prefix="/admin", tags=["Admin: Roles"])
api_router.include_router(stocks, prefix="/stocks", tags=["stocks"])
api_router.include_router(orders, prefix="/orders", tags=["orders"])
api_router.include_router(clients, prefix="/clients", tags=["OP_Colis: Clients"])
api_router.include_router(commune_router, prefix="/communes", tags=["Admin: Communes"])
api_router.include_router(commande_router, prefix="/commandes", tags=["OP_Colis: Commandes"])
api_router.include_router(conditionnement_router, prefix="/conditionnements", tags=["Conditionnements"])
# api_router.include_router(detail_commande_router, prefix="/details-commande", tags=["OP_Colis: Details Commande"])
api_router.include_router(departements, prefix="/departments", tags=["Admin: Departments"])
api_router.include_router(zip_codes, prefix="/zip-code", tags=["Admin: Zip Code"])

