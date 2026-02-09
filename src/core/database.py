from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from .config import settings

# Crear engine
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, echo=settings.DEBUG)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency to get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Importar todos los modelos aquí para que Base los registre
# Esto evita problemas con alembic
def import_models():
    # Los importaremos dinámicamente desde main.py
    pass
