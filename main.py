from fastapi import FastAPI
from routers.materials import router as materials_router
from database import Base, engine
from models import Material

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ForgeFlow API")

app.include_router(materials_router)


@app.get("/")
def home():
    return {"message": "ForgeFlow API is running"}