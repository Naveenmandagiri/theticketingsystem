from fastapi import APIRouter
from api.v1.auth import auth_router
from api.v1.user import user_router
from api.v1.clients.client import client_router
from api.v1.clients.contract import contract_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(user_router)
api_router.include_router(client_router)
<<<<<<< HEAD
=======
api_router.include_router(contract_router)
>>>>>>> c913065e723f985100b86fe41e0a58882ea379c3
