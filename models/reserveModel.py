from pydantic import BaseModel
from datetime import date
from typing import List

class ReserveModel(BaseModel):
    start_date: date
    end_date: date

    def overlaps(self, reserves: List["ReserveModel"]) -> bool:
        return any(
            (self.start_date <= reserve.end_date and self.end_date >= reserve.start_date)
            for reserve in reserves
        )