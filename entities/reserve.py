from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from databases.database import PostgresBase

from datetime import date

from entities.user import User
from models.reserveModel import ReserveModel

class Reserve(PostgresBase):
    __tablename__ = "reserves"

    def __init__(self, user: User, lodgment_id: str, start_date: date, end_date: date, cost: int):
        self.user = user
        self.lodgment_id = lodgment_id
        self.start_date = start_date
        self.end_date = end_date
        self.cost = cost

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    lodgment_id = Column(String, nullable=False)

    start_date = Column(Date, nullable=False)

    end_date = Column(Date, nullable=False)

    cost = Column(Integer, default=0)

    def overlaps(self, reserves: list["Reserve"]) -> bool:
        return any(
            (self.start_date <= other.end_date and self.end_date >= other.start_date)
            for other in reserves
        )
    
    def to_reserve_model(self) -> ReserveModel:
        return ReserveModel(
            self.start_date,
            self.end_date
        )