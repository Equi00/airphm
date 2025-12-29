from pydantic import BaseModel
from datetime import date, datetime, time
from typing import List

class ReserveModel(BaseModel):
    id: int
    start_date: date
    end_date: date

    def to_mongo(self) -> dict:
        return {
            "id": self.id,
            "start_date": datetime.combine(self.start_date, time.min),
            "end_date": datetime.combine(self.end_date, time.min),
        }

    def overlaps(self, reserves: List["ReserveModel"]) -> bool:
        return any(
            (self.start_date <= reserve.end_date and self.end_date >= reserve.start_date)
            for reserve in reserves
        )