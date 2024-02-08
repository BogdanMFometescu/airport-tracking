from dotenv import load_dotenv
from fastapi import FastAPI
from src.endpoints.ep_airport import airport_router
from src.endpoints.ep_airplane import airplane_router
from src.endpoints.ep_schedule import schedule_router
from src.endpoints.v1.ep_airplane_api import airplane_router_api
from src.endpoints.v1.ep_airport_api import airport_router_api
from src.endpoints.v1.ep_schedule_api import schedule_router_api
from src.storage.json_storage import JsonStorage

load_dotenv()

storage = JsonStorage()

app = FastAPI()

routers = [
    airport_router,
    airplane_router,
    schedule_router,
    airplane_router_api,
    airport_router_api,
    schedule_router_api
]

for router in routers:
    app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")
