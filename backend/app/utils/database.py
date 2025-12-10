"""Database connection management."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pymongo import MongoClient
from typing import Generator
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

# PostgreSQL Setup
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    echo=settings.DEBUG
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# MongoDB Setup
mongo_client = None
mongo_db = None


def get_mongo_client() -> MongoClient:
    """Get MongoDB client."""
    global mongo_client
    if mongo_client is None:
        mongo_client = MongoClient(settings.MONGODB_URL)
        logger.info("MongoDB connection established")
    return mongo_client


def get_mongo_db():
    """Get MongoDB database."""
    global mongo_db
    if mongo_db is None:
        client = get_mongo_client()
        mongo_db = client[settings.MONGODB_DB]
    return mongo_db


def close_mongo_connection():
    """Close MongoDB connection."""
    global mongo_client, mongo_db
    if mongo_client:
        mongo_client.close()
        mongo_client = None
        mongo_db = None
        logger.info("MongoDB connection closed")


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables initialized")


