from dateutil.relativedelta import relativedelta
import pytest
from pymongo import MongoClient
from datetime import date
from entities.rateData import RateData
from entities.accommodation import Department, House, Hut
from models.accommodationModel import AccommodationDetailModel
from models.reserveModel import ReserveModel

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
    reserve1 = ReserveModel(start_date=date.today(), end_date=date.today() + relativedelta(days=5))
    reserve2 = ReserveModel(start_date=date.today(), end_date=date.today() + relativedelta(days=15))

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

def test_to_detail_model_with_rates_and_reserves(session):
    """TODO: complete this test with rates"""
    reserve = ReserveModel(start_date=date.today(), end_date=date.today() + relativedelta(days=5))


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
        reserves=[reserve]
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