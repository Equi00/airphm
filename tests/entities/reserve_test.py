from databases.sql_database import PostgresBase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date
from dateutil.relativedelta import relativedelta
from entities.user import User
from models.reserveModel import ReserveModel
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

def test_create_reserve(session):
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

    reserve = Reserve(
        user=user_db,
        accommodation_id="L123",
        start_date=date.today(),
        end_date=date.today() + relativedelta(days=5),
        cost=200
    )

    session.add(reserve)
    session.commit()

    reserve_db = session.query(Reserve).first()

    assert reserve_db is not None
    assert reserve_db.accommodation_id == "L123"
    assert reserve_db.start_date == date.today()
    assert reserve_db.end_date == date.today() + relativedelta(days=5)
    assert reserve_db.cost == 200
    assert reserve_db.user_id == user_db.id

def test_overlaps_true():
    r1 = Reserve(None, "A1", date.today(), date.today() + relativedelta(days=5), 100)
    r2 = Reserve(None, "A1", date.today(), date.today() + relativedelta(days=15), 100)

    assert r1.overlaps([r2]) is True


def test_overlaps_false():
    r1 = Reserve(None, "A1", date.today(), date.today() + relativedelta(days=5), 100)
    r2 = Reserve(None, "A1", date.today() + relativedelta(days=10), date.today() + relativedelta(days=15), 100)


    assert r1.overlaps([r2]) is False


def test_overlaps_multiple_reserves():
    r1 = Reserve(None, "A1", date.today(), date.today() + relativedelta(days=5), 100)
    r2 = Reserve(None, "A1", date.today(), date.today() + relativedelta(days=10), 100)
    r3 = Reserve(None, "A1", date.today(), date.today() + relativedelta(days=15), 100)

    assert r1.overlaps([r2, r3]) is True


def test_to_reserve_model(session):
    user = User(
        name="Ezequiel",
        surname="Oyola",
        country="Argentina",
        balance=300,
        birthdate=date(2000, 6, 14)
    )

    session.add(user)
    session.commit()
    
    reserve = Reserve(user, "X1", date.today(), date.today() + relativedelta(days=5), 50)
    
    session.add(reserve)
    session.commit()

    reserve_db = session.query(Reserve).filter_by(accommodation_id="X1").first()
    
    reserve_model = reserve_db.to_reserve_model()

    assert isinstance(reserve_model, ReserveModel)


def test_overlaps_reserve_model_true(session):
    user = User(
        name="Ezequiel",
        surname="Oyola",
        country="Argentina",
        balance=300,
        birthdate=date(2000, 6, 14)
    )

    session.add(user)
    session.commit()
    
    r1 = Reserve(user, "A1", date.today(), date.today() + relativedelta(days=5), 100)
    r2 = Reserve(user, "A1", date.today(), date.today() + relativedelta(days=15), 100)

    session.add_all([r1,r2])
    session.commit()

    reserve_db = session.query(Reserve).filter_by(accommodation_id="A1").all()

    rm1 = reserve_db[0].to_reserve_model()
    rm2 = reserve_db[1].to_reserve_model()

    assert rm1.overlaps([rm2]) is True


def test_overlaps_reserve_model_false(session):
    user = User(
        name="Ezequiel",
        surname="Oyola",
        country="Argentina",
        balance=300,
        birthdate=date(2000, 6, 14)
    )

    session.add(user)
    session.commit()

    r1 = Reserve(user, "A1", date.today(), date.today() + relativedelta(days=5), 100)
    r2 = Reserve(user, "A1", date.today() + relativedelta(days=10), date.today() + relativedelta(days=15), 100)

    session.add_all([r1,r2])
    session.commit()

    reserve_db = session.query(Reserve).filter_by(accommodation_id="A1").all()

    rm1 = reserve_db[0].to_reserve_model()
    rm2 = reserve_db[1].to_reserve_model()

    assert rm1.overlaps([rm2]) is False


def test_overlaps_multiple_reserves_reserve_model(session):
    user = User(
        name="Ezequiel",
        surname="Oyola",
        country="Argentina",
        balance=300,
        birthdate=date(2000, 6, 14)
    )

    session.add(user)
    session.commit()

    r1 = Reserve(user, "A1", date.today(), date.today() + relativedelta(days=5), 100)
    r2 = Reserve(user, "A1", date.today(), date.today() + relativedelta(days=10), 100)
    r3 = Reserve(user, "A1", date.today(), date.today() + relativedelta(days=15), 100)

    session.add_all([r1,r2,r3])
    session.commit()

    reserve_db = session.query(Reserve).filter_by(accommodation_id="A1").all()

    rm1 = reserve_db[0].to_reserve_model()
    rm2 = reserve_db[1].to_reserve_model()
    rm3 = reserve_db[2].to_reserve_model()

    assert rm1.overlaps([rm2, rm3]) is True