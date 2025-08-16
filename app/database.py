"""
Database configuration and session management.
Uses SQLAlchemy for ORM and Alembic for migrations.
"""

import logging
import os
from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from alembic import command
from alembic.config import Config

from app.config import settings

logger = logging.getLogger(__name__)

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using
    pool_size=10,        # Number of connections to maintain
    max_overflow=20,     # Maximum overflow connections
    echo=False,          # Set to True for SQL query logging (debug only)
)

# Create SessionLocal class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create Base class for models
metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
)

Base = declarative_base(metadata=metadata)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get a database session.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def init_db() -> None:
    """
    Initialize database schema using Alembic migrations.
    Controlled by AUTO_MIGRATE env var:
        AUTO_MIGRATE=true -> run migrations automatically
        AUTO_MIGRATE=false (default) -> skip migrations
    """
    auto_migrate = os.getenv("AUTO_MIGRATE", "false").lower() == "true"
    if not auto_migrate:
        logger.info("AUTO_MIGRATE disabled — skipping automatic Alembic migrations")
        return

    try:
        alembic_cfg = Config(str(Path(__file__).parent.parent / "alembic.ini"))
        alembic_cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

        command.upgrade(alembic_cfg, "head")
        logger.info("Database migrated to latest revision using Alembic")
    except Exception as e:
        logger.error(f"Error running Alembic migrations: {e}")
        raise


def check_database_connection() -> bool:
    """
    Check if database is accessible.
    Used for health checks.
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False
