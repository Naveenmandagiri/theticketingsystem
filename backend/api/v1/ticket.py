from fastapi import APIRouter

ticket_router = APIRouter(prefix="/ticket", tags=["ticket"])

@ticket_router.get('/')
async def list_of_tickets():
    return "New file"