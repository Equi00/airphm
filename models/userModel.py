from pydantic import BaseModel
from datetime import date
from typing import List
from models.reserveModel import ReserveModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities.user import User

class FriendModel(BaseModel):
    id: int
    name: str
    surname: str

class UserModel(BaseModel):
    id: int
    name: str
    surname: str
    country: str
    balance: int
    birthdate: date
    email: str

class FullUserModel(BaseModel): # this will also be used for update the user
    id: int
    name: str
    surname: str
    country: str
    balance: int
    birthdate: date
    email: str
    reserves: List[ReserveModel]
    friends: List[FriendModel]

    def to_entity(self) -> "User":
        return User(
            self.id,
            self.name,
            self.surname,
            self.country,
            self.balance,
            self.birthdate,
            self.email,
            self.reserves,
            self.friends)

class UserResponse(BaseModel):
    id: int
    name: str

