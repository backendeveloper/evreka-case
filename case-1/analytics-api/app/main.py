import logging
from fastapi import FastAPI
from app.db.session import init_db
from app.routers import analytics

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Analytics API",
    version="1.0.0"
)


@app.on_event("startup")
async def startup_event():
    await init_db()
    logger.info("Database tables created.")


app.include_router(analytics.router)
