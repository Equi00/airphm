from databases.sql_database import PostgresBase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dateutil.relativedelta import relativedelta
import pytest
from pymongo import MongoClient
from datetime import date
from entities.rateData import RateData
from entities.accommodation import Department, House, Hut
from entities.user import User
from entities.reserve import Reserve
from models.accommodationModel import AccommodationDetailModel
from models.reserveModel import ReserveModel

DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

@pytest.fixture(scope="function")
def session_postgres():
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

@pytest.fixture(scope="function")
def session():
    client = MongoClient("localhost", 27017)

    db = client.Airphm_test_db
    collection = db.accomodation

    collection.delete_many({})

    yield collection

    collection.delete_many({})
    client.close()

def test_create_accommodation(session):
    hut = Hut(
        owner_id=1,
        base_cost=10000,
        name="Mountain Hut",
        description="Nice hut",
        capacity=4,
        bedrooms=2,
        bathrooms=1,
        accommodation_detail="Wood cabin",
        other_aspects="Fireplace",
        cleaning_service=True,
        address="Hill 123",
        country="Argentina",
        image_url="img.jpg",
        reserves=[]
    )

    result = session.insert_one(hut.model_dump())

    assert result.inserted_id is not None

    saved = session.find_one({"_id": result.inserted_id})
    assert saved["type"] == "Hut"
    assert saved["name"] == "Mountain Hut"

def test_total_cost_hut():
    hut = Hut(
        owner_id=1,
        base_cost=10000,
        name="Mountain Hut",
        description="Nice hut",
        capacity=4,
        bedrooms=2,
        bathrooms=1,
        accommodation_detail="Wood cabin",
        other_aspects="Fireplace",
        cleaning_service=True,
        address="Hill 123",
        country="Argentina",
        image_url="img.jpg",
        reserves=[]
    )

    assert hut.total_cost() == 21000

def test_total_cost_house():
    house = House(
        owner_id=1,
        base_cost=10000,
        name="House",
        description="Desc",
        capacity=4,
        bedrooms=2,
        bathrooms=1,
        accommodation_detail="Detail",
        other_aspects="Other",
        cleaning_service=False,
        address="Addr",
        country="AR",
        image_url="img",
        reserves=[]
    )

    assert house.total_cost() == 12600

def test_total_cost_department():
    department = Department(
        owner_id=1,
        base_cost=10000,
        name="Department",
        description="Desc",
        capacity=4,
        bedrooms=2,
        bathrooms=1,
        accommodation_detail="Detail",
        other_aspects="Other",
        cleaning_service=False,
        address="Addr",
        country="AR",
        image_url="img",
        reserves=[]
    )

    assert department.total_cost() == 14700

    department.bedrooms = 3

    assert department.total_cost() == 13650

def test_is_valid_true():
    acc = Hut(
        owner_id=1,
        base_cost=10000,
        name="Mountain Hut",
        description="Nice hut",
        capacity=4,
        bedrooms=2,
        bathrooms=1,
        accommodation_detail="Wood cabin",
        other_aspects="Fireplace",
        cleaning_service=True,
        address="Hill 123",
        country="Argentina",
        image_url="img.jpg",
        reserves=[]
    )

    assert acc.is_valid() is True

def test_is_valid_false_missing_name():
    acc = Hut(
        owner_id=1,
        base_cost=10000,
        name="",
        description="Nice hut",
        capacity=4,
        bedrooms=2,
        bathrooms=1,
        accommodation_detail="Wood cabin",
        other_aspects="Fireplace",
        cleaning_service=True,
        address="Hill 123",
        country="Argentina",
        image_url="img.jpg",
        reserves=[]
    )

    assert acc.is_valid() is False

def test_find_by_type(session):
    hut = Hut(
        owner_id=1,
        base_cost=10000,
        name="Mountain Hut",
        description="Nice hut",
        capacity=4,
        bedrooms=2,
        bathrooms=1,
        accommodation_detail="Wood cabin",
        other_aspects="Fireplace",
        cleaning_service=True,
        address="Hill 123",
        country="Argentina",
        image_url="img.jpg",
        reserves=[]
    )

    session.insert_one(hut.model_dump())

    found = session.find_one({"type": "Hut"})
    assert found is not None

def test_has_overlapped_reserves_without_reserves():
    hut = Hut(
        owner_id=1,
        base_cost=10000,
        name="Mountain Hut",
        description="Nice hut",
        capacity=4,
        bedrooms=2,
        bathrooms=1,
        accommodation_detail="Wood cabin",
        other_aspects="Fireplace",
        cleaning_service=True,
        address="Hill 123",
        country="Argentina",
        image_url="img.jpg",
        reserves=[]
    )

    assert hut.has_overlapped_reserves() is False

def test_has_overlapped_reserves_false():
    reserve1 = ReserveModel(id=1, start_date=date.today(), end_date=date.today() + relativedelta(days=5))
    reserve2 = ReserveModel(id=2, start_date=date.today(), end_date=date.today() + relativedelta(days=15))

    hut = Hut(
        owner_id=1,
        base_cost=10000,
        name="Mountain Hut",
        description="Nice hut",
        capacity=4,
        bedrooms=2,
        bathrooms=1,
        accommodation_detail="Wood cabin",
        other_aspects="Fireplace",
        cleaning_service=True,
        address="Hill 123",
        country="Argentina",
        image_url="img.jpg",
        reserves=[reserve1, reserve2]
    )

    assert hut.has_overlapped_reserves() is True

def test_to_detail_model_without_rates(session):
    hut = Hut(
        owner_id=1,
        base_cost=10000,
        name="Mountain Hut",
        description="Nice hut",
        capacity=4,
        bedrooms=2,
        bathrooms=1,
        accommodation_detail="Wood cabin",
        other_aspects="Fireplace",
        cleaning_service=True,
        address="Hill 123",
        country="Argentina",
        image_url="img.jpg",
        reserves=[]
    )

    result = session.insert_one(hut.model_dump())

    assert result.inserted_id is not None

    saved = session.find_one({"_id": result.inserted_id})

    saved["id"] = str(saved["_id"])
    del saved["_id"]

    saved_entity = Hut.model_validate(saved)

    acc_model = saved_entity.to_detail_model([])

    assert type(acc_model) is AccommodationDetailModel
    assert "Hut" is acc_model.type

def test_to_detail_model_with_rates_and_reserves(session, session_postgres):
    reserve = ReserveModel(
        id=1,
        start_date=date.today(),
        end_date=date.today() + relativedelta(days=5)
    )

    user = User(
        name="Ezequiel",
        surname="Oyola",
        country="Argentina",
        balance=300,
        birthdate=date(2000, 6, 14)
    )
    session_postgres.add(user)
    session_postgres.commit()

    rate = RateData(
        user_rate=user,
        accommodation_rate_id="asdf",
        rate_score=3,
        commentary="Medium",
    )
    session_postgres.add(rate)
    session_postgres.commit()

    hut = Hut(
        owner_id=1,
        base_cost=10000,
        name="Mountain Hut",
        description="Nice hut",
        capacity=4,
        bedrooms=2,
        bathrooms=1,
        accommodation_detail="Wood cabin",
        other_aspects="Fireplace",
        cleaning_service=True,
        address="Hill 123",
        country="Argentina",
        image_url="img.jpg",
        reserves=[reserve],
    )

    saved = hut.to_mongo()
    saved["id"] = str(session.insert_one(saved).inserted_id)

    hut_entity = Hut.model_validate(saved)
    acc_model = hut_entity.to_detail_model([rate])

    assert isinstance(acc_model, AccommodationDetailModel)
    assert acc_model.type == "Hut"
    assert reserve in acc_model.reserves

    saved_rate = acc_model.rates[0]
    assert saved_rate.user.name == user.name
    assert saved_rate.user.surname == user.surname