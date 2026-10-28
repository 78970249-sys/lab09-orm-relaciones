import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from modelos import Base


@pytest.fixture(scope="function")
def db_session():
    """Entrega una sesión limpia en memoria para cada prueba."""
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()
        engine.dispose()