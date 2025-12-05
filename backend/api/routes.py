from fastapi import APIRouter
from api.v1.auth import auth_router
from api.v1.ticket import ticket_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(ticket_router)