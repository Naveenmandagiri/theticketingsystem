from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class Client(BaseModel):
    id: int
    idnumber: Optional[int] = None
    name: str
    email: str
    phone: int
    address: Optional[str] = None
    startdate: Optional[date] = None
    enddate: Optional[date] = None
    created_by_id: int
    modified_by_id: int

class Client_users(BaseModel):
    id: int
    user_id: int
    client_id: int

class Client_contracts(BaseModel):
    id: int
    client_id: int
    startdate: Optional[date] = None
    enddate: Optional[date] = None
    hours: int
    frequency: int
    status: bool = True
    created_by_id: int
    modified_by_id: int
