from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from contextlib import asynccontextmanager
import asyncio
from app.api import version, temperature, store, health
from app.services.sensebox import extract_recent_temperatures, fetch_sensebox_data
from app.services.storage import store_sensor_data
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: start background task
    await asyncio.sleep(5) # timeout to give porbes time to succeed 
    task = asyncio.create_task(periodic_store_task())
    yield
    # Shutdown: cancel task
    task.cancel()


async def periodic_store_task():
    while True:
        try:
            all_data = {}
            for box_id in settings.sensebox_ids:
                data = await fetch_sensebox_data(box_id)
                temps = extract_recent_temperatures(data)
                all_data[box_id] = temps
            store_sensor_data(all_data)
        except Exception as e:
            # Log error but keep running
            print(f"Storage task error: {e}")
        
        await asyncio.sleep(300)  # 5 minutes

app = FastAPI()
app.include_router(router=version.router)
app.include_router(router=temperature.router)
# app.include_router(router=store.router)
app.include_router(router=health.router)

Instrumentator().instrument(app).expose(app)


@app.get("/")
async def root():
    return {"message": "HiveBox API running"}
