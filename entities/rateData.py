from datetime import date
from sqlalchemy import Column, ForeignKey, String, Integer, Date
from sqlalchemy.orm import relationship
from databases.sql_database import PostgresBase

class RateData(PostgresBase):
    __tablename__ = "rate_data"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, unique=True)
    
    user_rate = relationship("User", uselist=False)

    accommodation_rate_id = Column(String, nullable=False)

    rate_score = Column(Integer, nullable=False)

    commentary = Column(String, nullable=False)

    rate_date = Column(Date, default=date.today)

    def is_valid(self) -> bool:
        return 1 <= self.rate_score <= 5