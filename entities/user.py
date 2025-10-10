from sqlalchemy import Table, Column, ForeignKey, String, Integer, Date
from sqlalchemy.orm import relationship
from databases.database import PostgresBase
from datetime import date
from dateutil.relativedelta import relativedelta

from models.userModel import FriendModel, FullUserModel, UserModel, UserResponse

user_friends = Table(
    "user_friends", # table name
    PostgresBase.metadata, # metadata
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("frind_id", Integer, ForeignKey("user.id"), primary_key=True)

)

class User(PostgresBase):
    __tablename__ = "user"

    def __init__(self, name: str, surname: str, country: str, balance: int, birthdate: date):
        self.name = name
        self.surname = surname
        self.country = country
        self.balance = balance
        self.birthdate = birthdate

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String(50), nullable=False)

    surname = Column(String(50), nullable=False)

    country = Column(String(50), nullable=False)

    balance = Column(Integer, default=0)

    birthdate = Column(Date, default=date.today())

    # when a user is deleted, all the reserves are deleted.
    reserves = relationship("Reserve", back_populates="user", cascade="all, delete-orphan", lazy="select")

    friends = relationship(
        "User",
        secondary=user_friends, 
        primaryjoin=id == user_friends.c.user_id,
        secondaryjoin=id == user_friends.c.friend_id
    )

    email = Column(String(75), default="")

    password = Column(String, default="")

    # lodgmentReserve TODO

    # rateLodgment TODO

    def recharge(self, cash: int):
        balance += cash

    def add_friend(self, user: "User"):
        if not self.isFriend(user):
            self.friends.append(user)

    def remove_friend(self, user: "User"):
        if self.isFriend(user):
            self.friends.remove(user)

    def is_friend(self, user: "User") -> bool:
        return user in self.friends
    
    def age(self) -> int:
        return relativedelta(date.today(), self.birthdate).years
    
    def is_valid(self) -> bool:
        return all[
            self.name.strip(),
            self.surname.strip(),
            self.country.strip(),
            self.balance >= 0,
            self.age() >= 18
        ]

    def user_to_Model(self) -> UserModel:
        return UserModel(
            id = self.id,
            name = self.name,
            surname = self.surname,
            country = self.country,
            balance = self.balance,
            birthdate = self.birthdate,
            email = self.email
        )
    
    def to_update_model(self) -> FullUserModel:
        return FullUserModel(
            id = self.id,
            name = self.name,
            surname = self.surname,
            country = self.country,
            balance = self.balance,
            birthdate = self.birthdate,
            email = self.email,
            #reserves = self.reserves, TODO
            friends = [self.friend.to_friend_dto() for friend in self.friends]
        )
    
    def to_friend_model(self) -> FriendModel:
        return FriendModel(
            id = self.id,
            name = self.name,
            surname = self.surname
        )

    def to_response(self) -> UserResponse:
        return UserResponse(id = self.id, name = self.name)
    
    #def has_overlapped_reserves() TODO

    #def _can_reserve() TODO
        
    #def _can_rate_lodgment() TODO