from fastapi import FastAPI
from app.api import version, temperature 
from app.core.config import settings

app = FastAPI()
app.include_router(router=version.router)
app.include_router(router=temperature.router)


@app.get("/")
async def root():
    return {"message": "HiveBox API running"}
