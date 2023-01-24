from fastapi import FastAPI
from core.config import settings
from endpoint.location import location_router
import uvicorn


app = FastAPI()

app.include_router(location_router, tags=["Location"], prefix="/api/locationservice")

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, log_level=settings.LOGLEVEL)
