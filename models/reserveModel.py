from pydantic import BaseModel
from datetime import date
from typing import List

class ReserveModel(BaseModel):
    def __init__(self, start_date: date, end_date: date):
        self.start_date = start_date
        self.end_date = end_date

    def overlaps(self, reserves: List["ReserveModel"]) -> bool:
        return any(
            (self.start_date <= reserve.end_date and self.end_date >= reserve.start_date)
            for reserve in reserves
        )