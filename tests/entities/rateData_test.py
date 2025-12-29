from databases.sql_database import PostgresBase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date
from entities.rateData import RateData
from entities.user import User
from entities.reserve import Reserve
import pytest

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

@pytest.fixture(scope="function")
def session():
    """Create a clean session for each test."""

    PostgresBase.metadata.create_all(bind=engine)
    db_session = SessionLocal()

    try:
        yield db_session
    finally:
        if db_session.is_active:
            db_session.rollback()

        db_session.close()

        PostgresBase.metadata.drop_all(bind=engine)

def test_create_rateData(session):
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


    rateData = RateData(
        user_rate=user_db,
        accommodation_rate_id="asdf",
        rate_score=3,
        commentary="Medium",
    )

    session.add(rateData)
    session.commit()

    rateData_db = session.query(RateData).filter_by(accommodation_rate_id="asdf").first()

    assert rateData_db is not None
    assert rateData_db.commentary == "Medium"
    assert rateData_db.rate_score == 3
    assert rateData_db.user_id == user_db.id

def test_is_valid_false(session):
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


    rateData = RateData(
        user_rate=user_db,
        accommodation_rate_id="asdf",
        rate_score=0,
        commentary="Medium",
    )

    rateData2 = RateData(
        user_rate=user_db,
        accommodation_rate_id="asdf",
        rate_score=9999,
        commentary="Medium",
    )

    assert rateData.is_valid() is False
    assert rateData2.is_valid() is False

def test_is_valid_true(session):
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


    rateData = RateData(
        user_rate=user_db,
        accommodation_rate_id="asdf",
        rate_score=3,
        commentary="Medium",
    )

    assert rateData.is_valid() is True
