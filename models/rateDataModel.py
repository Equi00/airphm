from pydantic import BaseModel
from datetime import date

from models.userModel import UserModel


class RateDataModel(BaseModel):
    score: int
    commentary: str
    user_id: int


class RateDataCommentModel(BaseModel):
    score: int
    commentary: str
    user: UserModel
    rate_date: date