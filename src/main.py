from dotenv import load_dotenv
from fastapi import FastAPI
from src.api.endpoints.v1.airplane_endpoint import airplane_router_api
from src.api.endpoints.v1.airport_endpoint import airport_router_api
from src.api.endpoints.v1.schedule_endpoint import schedule_router_api

load_dotenv()

app = FastAPI()

routers = [
    airplane_router_api,
    airport_router_api,
    schedule_router_api
]

for router in routers:
    app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")
