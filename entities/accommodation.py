from abc import ABC, abstractmethod
from typing import List, Literal
from pydantic import BaseModel, Field
from math import ceil

from entities.rateData import RateData
from models.accommodationModel import AccommodationDetailModel
from models.rateDataModel import RateDataCommentModel
from models.reserveModel import ReserveModel

class Accommodation(BaseModel, ABC):
    id: str | None = None
    type: str

    owner_id: int
    base_cost: int
    name: str
    description: str
    capacity: int
    bedrooms: int
    bathrooms: int
    accommodation_detail: str
    other_aspects: str
    cleaning_service: bool
    address: str
    country: str
    image_url: str

    reserves: List[ReserveModel] = []
    commission: float = 1.05
    rate_average: float = 0.0
    rate_count: int = 0

    @abstractmethod
    def plus(self) -> int:
        pass

    def total_cost(self) -> int:
        return ceil((self.base_cost + self.plus()) * self.commission)

    def has_overlapped_reserves(self) -> bool:
        if len(self.reserves) <= 1:
            return False

        for reserve in self.reserves:
            remaining = [r for r in self.reserves if r != reserve]
            if reserve.overlaps(remaining):
                return True
        return False

    def is_valid(self) -> bool:
        return bool(
            self.base_cost > 0
            and self.name.strip()
            and self.description.strip()
            and self.capacity > 0
            and self.bedrooms > 0
            and self.bathrooms > 0
            and self.accommodation_detail.strip()
            and self.other_aspects.strip()
            and self.address.strip()
            and self.country.strip()
            and self.image_url.strip()
            and not self.has_overlapped_reserves()
        )
    
    def to_detail_model(self, rates: list[RateData]) -> AccommodationDetailModel:
        return AccommodationDetailModel(
            id=self.id,
            owner_id=self.owner_id,
            name=self.name,
            description=self.description,
            base_cost=self.base_cost,
            capacity=self.capacity,
            bedrooms=self.bedrooms,
            bathrooms=self.bathrooms,
            accommodation_detail=self.accommodation_detail,
            other_aspects=self.other_aspects,
            cleaning_service=self.cleaning_service,
            address=self.address,
            country=self.country,
            image_url=self.image_url,
            reserves=self.reserves,
            rates=[
                RateDataCommentModel(
                    rate_score=rate.rate_score,
                    commentary=rate.commentary,
                    user=rate.user_rate.to_user_model(),
                    rate_date=rate.rate_date
                )
                for rate in rates
            ],
            rate_average=self.rate_average,
            rate_count=self.rate_count,
            commission=self.commission,
            type=self.__class__.__name__
        )
    
    def to_mongo(self) -> dict:
        data = self.model_dump()
        data["reserves"] = [r.to_mongo() for r in self.reserves]
        return data
    
class Hut(Accommodation):
    type: Literal["Hut"] = "Hut"

    def plus(self) -> int:
        return 10000 if self.cleaning_service else 0
    
class House(Accommodation):
    type: Literal["House"] = "House"

    def plus(self) -> int:
        return self.capacity * 500
    
class Department(Accommodation):
    type: Literal["Department"] = "Department"

    def plus(self) -> int:
        if self.bedrooms < 3:
            return 2000 * self.bedrooms
        return 1000 * self.bedrooms