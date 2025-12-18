from pydantic import BaseModel, Field
import datetime

class RateData(BaseModel):
    user_id: int
    accommodation_rate_id: str
    rate_score: int
    commentary: str
    date: datetime = Field(default_factory=datetime.date.today)

    def is_valid(self) -> bool:
        return 1 <= self.rate_score <= 5