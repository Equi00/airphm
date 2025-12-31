from databases.sql_database import PostgresBase
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date
from dateutil.relativedelta import relativedelta
from entities.accommodation import Hut
from entities.user import User
from entities.rateData import RateData
from exceptions.badRequestException import BadRequestException
from models.userModel import UserModel, FriendModel, UserResponse, FullUserModel
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

def test_add_friend(session):
    user1 = User(
        name="Ezequiel",
        surname="Oyola",
        country="Argentina",
        balance=300,
        birthdate=date(2000, 6, 14)
    )

    user2 = User(
        name="Jorge",
        surname="Lampara",
        country="Chile",
        balance=0,
        birthdate=date(2010, 7, 18)
    )

    session.add_all([user1,user2])
    session.commit()

    user1.add_friend(user2)
    session.commit()

    user_db = session.query(User).filter_by(name="Ezequiel").first()

    assert user2 in user1.friends
    assert user_db.is_friend(user2)

def test_remove_friend(session):
    user1 = User(
        name="Ezequiel",
        surname="Oyola",
        country="Argentina",
        balance=300,
        birthdate=date(2000, 6, 14)
    )

    user2 = User(
        name="Jorge",
        surname="Lampara",
        country="Chile",
        balance=0,
        birthdate=date(2010, 7, 18)
    )

    session.add_all([user1,user2])
    session.commit()

    user1.add_friend(user2)
    session.commit()

    user1.remove_friend(user2)
    session.commit()

    user_db = session.query(User).filter_by(name="Ezequiel").first()

    assert user2 not in user1.friends
    assert not user_db.is_friend(user2)

def test_age_calculation():
    birthdate = date.today() - relativedelta(years=25)
    user = User(
        name="Ezequiel",
        surname="Oyola",
        country="Argentina",
        balance=300,
        birthdate=birthdate
    )

    assert user.age() == 25

def test_is_valid_user_true():
    birthdate = date.today() - relativedelta(years=25)
    user = User(
        name="Ezequiel",
        surname="Oyola",
        country="Argentina",
        balance=300,
        birthdate=birthdate
    )

    assert user.is_valid() is True

def test_is_valid_user_false():
    birthdate = date.today() - relativedelta(years=25)
    user = User(
        name="",
        surname="Oyola",
        country="Argentina",
        balance=300,
        birthdate=birthdate
    )

    assert user.is_valid() is False

def test_recharge_balance(session):
    birthdate = date.today() - relativedelta(years=25)
    user = User(
        name="Ezequiel",
        surname="Oyola",
        country="Argentina",
        balance=300,
        birthdate=birthdate
    )

    session.add(user)
    session.commit()

    user.recharge(50)
    session.commit()

    user_db = session.query(User).filter_by(name="Ezequiel").first()

    assert user_db.balance == 350

def test_to_user_model(session):
    birthdate = date.today() - relativedelta(years=25)
    user = User(
        name="Ezequiel",
        surname="Oyola",
        country="Argentina",
        balance=300,
        birthdate=birthdate
    )

    user.email = "somethin@gmail.com"

    session.add(user)
    session.commit()

    user_db = session.query(User).filter_by(name="Ezequiel").first()

    user_model = user_db.to_user_model()

    assert isinstance(user_model, UserModel)

def test_to_friend_model(session):
    birthdate = date.today() - relativedelta(years=25)
    user = User(
        name="Ezequiel",
        surname="Oyola",
        country="Argentina",
        balance=300,
        birthdate=birthdate
    )

    session.add(user)
    session.commit()

    user_db = session.query(User).filter_by(name="Ezequiel").first()

    user_model = user_db.to_friend_model()

    assert isinstance(user_model, FriendModel)

def test_to_response_model(session):
    birthdate = date.today() - relativedelta(years=25)
    user = User(
        name="Ezequiel",
        surname="Oyola",
        country="Argentina",
        balance=300,
        birthdate=birthdate
    )

    session.add(user)
    session.commit()

    user_db = session.query(User).filter_by(name="Ezequiel").first()

    user_model = user_db.to_response()

    assert isinstance(user_model, UserResponse)

def test_to_update_model(session):
    birthdate = date.today() - relativedelta(years=25)
    user = User(
        name="Ezequiel",
        surname="Oyola",
        country="Argentina",
        balance=300,
        birthdate=birthdate
    )

    session.add(user)
    session.commit()

    user_db = session.query(User).filter_by(name="Ezequiel").first()

    user_model = user_db.to_update_model()

    assert isinstance(user_model, FullUserModel)

def test_has_overlapped_reserves_false():
    birthdate = date.today() - relativedelta(years=25)
    user = User(
        name="Ezequiel",
        surname="Oyola",
        country="Argentina",
        balance=300,
        birthdate=birthdate
    )

    assert user.has_overlapped_reserves() is False

def test_has_overlapped_reserves_true():
    birthdate = date.today() - relativedelta(years=25)
    user = User(
        name="Ezequiel",
        surname="Oyola",
        country="Argentina",
        balance=300,
        birthdate=birthdate
    )

    reserve1 = Reserve(
        user=user, 
        accommodation_id="232344",
        start_date=(date.today() - relativedelta(days=10)),
        end_date=date.today(),
        cost=200)
    
    reserve2 = Reserve(
        user=user, 
        accommodation_id="55555",
        start_date=(date.today() - relativedelta(days=5)),
        end_date=date.today(),
        cost=200)
    
    user.reserves = [reserve1, reserve2]

    assert user.has_overlapped_reserves() is True

def test_when_delete_user_delete_reserves(session):
    birthdate = date.today() - relativedelta(years=25)
    user = User(
        name="Ezequiel",
        surname="Oyola",
        country="Argentina",
        balance=300,
        birthdate=birthdate
    )

    reserve1 = Reserve(
        user=user, 
        accommodation_id="232344",
        start_date=(date.today() - relativedelta(days=10)),
        end_date=date.today(),
        cost=200)
    
    reserve2 = Reserve(
        user=user, 
        accommodation_id="55555",
        start_date=(date.today() - relativedelta(days=5)),
        end_date=date.today(),
        cost=200)
    
    user.reserves = [reserve1, reserve2]

    session.add(user)
    session.commit()

    user_db = session.query(User).filter_by(name="Ezequiel").first()
    reserve_db1 = session.query(Reserve).filter_by(user_id=user_db.id).first()

    assert reserve_db1.accommodation_id == "232344"

    session.delete(user_db)
    session.commit()

    user_db = session.query(User).filter_by(name="Ezequiel").first()
    reserve_db1 = session.query(Reserve).filter_by(accommodation_id=232344).first()

    assert user_db is None
    assert reserve_db1 is None

def test_when_delete_user_delete_rates(session):
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


    rateData1 = RateData(
        user_rate=user_db,
        accommodation_rate_id="asdf",
        rate_score=3,
        commentary="Medium",
    )

    rateData2 = RateData(
        user_rate=user_db,
        accommodation_rate_id="asdf",
        rate_score=3,
        commentary="Medium",
    )
    
    session.add_all([rateData1, rateData2])
    session.commit()

    rateData_db1 = session.query(RateData).filter_by(accommodation_rate_id="asdf").first()

    assert rateData_db1.accommodation_rate_id == "asdf"

    session.delete(user_db)
    session.commit()

    user_db = session.query(User).filter_by(name="Ezequiel").first()
    rateData_db1 = session.query(RateData).filter_by(accommodation_rate_id="asdf").first()

    assert user_db is None
    assert rateData_db1 is None

def test_accommodation_reserve_success():
    user = User(
        name="Ezequiel",
        surname="Oyola",
        country="Argentina",
        balance=5000,
        birthdate=date(2000, 6, 14)
    )

    user.accommodation_reserve(
        accommodation_id="A1",
        start_date=date.today(),
        end_date=date.today() + relativedelta(days=3),
        total_cost=2000
    )

    assert len(user.reserves) == 1
    assert user.reserves[0].accommodation_id == "A1"
    assert user.balance == 3000

def test_accommodation_reserve_insufficient_balance():
    user = User(
        name="Ezequiel",
        surname="Oyola",
        country="Argentina",
        balance=1000,
        birthdate=date(2000, 6, 14)
    )

    with pytest.raises(BadRequestException):
        user.accommodation_reserve(
            accommodation_id="A1",
            start_date=date.today(),
            end_date=date.today() + relativedelta(days=3),
            total_cost=2000
        )

    assert len(user.reserves) == 0

def test_accommodation_reserve_same_accommodation_twice():
    user = User(
        name="Ezequiel",
        surname="Oyola",
        country="Argentina",
        balance=5000,
        birthdate=date(2000, 6, 14)
    )

    user.accommodation_reserve(
        accommodation_id="A1",
        start_date=date.today(),
        end_date=date.today() + relativedelta(days=3),
        total_cost=1000
    )

    with pytest.raises(BadRequestException):
        user.accommodation_reserve(
            accommodation_id="A1",
            start_date=date.today(),
            end_date=date.today() + relativedelta(days=5),
            total_cost=1000
        )

def test_rate_accommodation_success():
    user = User(
        name="Ezequiel",
        surname="Oyola",
        country="Argentina",
        balance=5000,
        birthdate=date(2000, 6, 14)
    )

    hut = Hut(
        id="A1",
        owner_id=1,
        base_cost=1000,
        name="Mountain Hut",
        description="Nice",
        capacity=2,
        bedrooms=1,
        bathrooms=1,
        accommodation_detail="Detail",
        other_aspects="Other",
        cleaning_service=False,
        address="Addr",
        country="AR",
        image_url="img"
    )

    user.accommodation_reserve(
        accommodation_id="A1",
        start_date=date.today(),
        end_date=date.today() + relativedelta(days=3),
        total_cost=1000
    )

    user.rate_accommodation(hut, score=4, commentary="Nice place")

    assert hut.rate_count == 1
    assert hut.rate_average == 4

def test_rate_accommodation_not_reserved():
    user = User(
        name="Ezequiel",
        surname="Oyola",
        country="Argentina",
        balance=5000,
        birthdate=date(2000, 6, 14)
    )

    hut = Hut(
        id="A1",
        owner_id=1,
        base_cost=1000,
        name="Mountain Hut",
        description="Nice",
        capacity=2,
        bedrooms=1,
        bathrooms=1,
        accommodation_detail="Detail",
        other_aspects="Other",
        cleaning_service=False,
        address="Addr",
        country="AR",
        image_url="img"
    )

    with pytest.raises(BadRequestException):
        user.rate_accommodation(hut, score=5, commentary="Great!")