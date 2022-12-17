from fastapi import FastAPI
from core.config import settings
# from endpoint.device import device_router
from starlette.responses import RedirectResponse
import uvicorn


app = FastAPI()


# @app.get("/", include_in_schema=False)
# def docs():  # skipcq: PTC-W0065
#     return RedirectResponse(url="/docs/")


# app.include_router(device_router, tags=["Device"], prefix="/api/deviceservice")


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, log_level=settings.LOGLEVEL)

