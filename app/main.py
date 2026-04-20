from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from app.api import version, temperature

app = FastAPI()
app.include_router(router=version.router)
app.include_router(router=temperature.router)

Instrumentator().instrument(app).expose(app)


@app.get("/")
async def root():
    return {"message": "HiveBox API running"}
