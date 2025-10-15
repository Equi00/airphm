from databases.database import PostgresBase, PostgresSessionLocal, postgres_engine
from datetime import date
from entities.user import User
from entities.reserve import Reserve
import pytest

@pytest.fixture(scope="function")
def session():
    """Create a clean sessio for each test."""

    PostgresBase.metadata.create_all(bind=postgres_engine)
    db_session = PostgresSessionLocal()

    try:
        yield db_session
    finally:
        if db_session.is_active:
            db_session.rollback()

        db_session.close()

        PostgresBase.metadata.drop_all(bind=postgres_engine)

def test_create_user(session):
    user = User(
        name="Ezequiel",
        surname="Oyola",
        country="Argentina",
        balance=300,
        birthdate=date(2000, 6, 14)
    )

    session.add(user)
    session.commit()

    user_db = session.query(User).filter_by(name="Ezequiel").first()

    assert user_db is not None
    assert user_db.name == "Ezequiel"
    assert user_db.balance == 300