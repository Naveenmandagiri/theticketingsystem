from fastapi import APIRouter, Depends, HTTPException
from db.db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db.models.clients import Clients as client_model, Client_contracts as contract_model, Client_users as userlink_model
from db.schemas.clients import Client
from datetime import datetime

client_router = APIRouter(prefix="/clients", tags=["clients"])

@client_router.get("/")
async def get_all_clients(db: AsyncSession = Depends(get_async_session)):
    results = await db.execute(select(client_model))
    records = results.scalars().all()
    if records:
        return records
    else:
        return "There is no Clients"

@client_router.get("/client/{id}")
async def get_client(id: int, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(client_model).where(client_model.id == id))
    record = result.scalar()
    if record:
        return record
    else:
        return "No client found"

@client_router.post("/clients/")
async def add_client(client: Client, db: AsyncSession = Depends(get_async_session)):
    data = client.model_dump()
    now = datetime.now().replace(microsecond=0)
    data["created_at"] = data.get("created_at") or now
    data["modified_at"] = now
    clientobj = client_model(**data)
    db.add(clientobj)
    
    try:
        await db.flush()
        contract = contract_model(
            client_id = clientobj.id,
            startdate = data["startdate"],
            enddate   = data["enddate"],
            hours     = None,
            frequency = 2,
            status    = True,
            created_by_id = data.get("created_by_id"),
            modified_by_id = data.get("modified_by_id"),
            created_at = now,
            modified_at = now
        )
        db.add(contract)

        if data.get("created_by_id") is not None:
            cu = userlink_model(
                user_id = data["created_by_id"],
                client_id = clientobj.id
            )
            db.add(cu)

        await db.commit()
        await db.refresh(clientobj)

        return clientobj
    except Exception as exc:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(exc))

@client_router.put("/client/{id}")
async def update_client(id: int, client: Client, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(client_model).where(client_model.id == id))
    record = result.scalar_one_or_none()
    if record:
        record.name = client.name
        record.phone = client.phone
        record.address = client.address
        record.startdate = client.startdate
        record.enddate = client.enddate
        record.modified_by_id = client.modified_by_id
        now = datetime.now().replace(microsecond=0)
        record.modified_at = now
        try:

            await db.flush()
            result = await db.execute(
                select(contract_model).where(contract_model.client_id == id).order_by(contract_model.id.desc()).limit(1)
            )
            contract = result.scalar_one_or_none()
            if contract:
                contract.startdate = client.startdate
                contract.enddate = client.enddate
                contract.hours = 10
                contract.frequency = 2
                contract.status = True
                contract.modified_by_id = client.modified_by_id
                contract.modified_at = now
            else:
                new_contract = contract_model(
                    client_id = id,
                    startdate = client.startdate,
                    enddate   = client.enddate,
                    hours     = 10,
                    frequency = 2,
                    status    = True,
                    created_by_id = client.modified_by_id,
                    modified_by_id = client.modified_by_id,
                    created_at = now,
                    modified_at = now
                )
                db.add(new_contract)

            await db.commit()
            await db.refresh(record)
            return record
        except Exception as exc:
            await db.rollback()
            raise HTTPException(status_code=400, detail=str(exc))
    else:
        return "Client no found"

@client_router.delete("client/{id}")
async def delete_client(id: int, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(client_model).where(client_model.id == id))
    record = result.scalar_one_or_none()
    if record:
        try:
            await db.delete(record)
            await db.commit()
            return {"message": "Client deleted successfully"}
        except Exception as exc:
            await db.rollback()
            raise HTTPException(status_code=400, detail=str(exc))
    else:
        return "Client not found"