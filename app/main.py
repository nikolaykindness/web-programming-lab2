from fastapi import FastAPI
from app.api.router import router
from app.config import DATABASE_URL

app = FastAPI(title="Уголок читателя", version="1.0.0")
app.include_router(router)

print(f"Using database: {DATABASE_URL}")  # увидишь URL в терминале при старте