from fastapi import FastAPI
from utils.settings import config
from utils.initialize import lifespan
from api.routes import api_router

app = FastAPI(lifespan=lifespan)


app.include_router(api_router)

@app.get('/')
def index():
    return