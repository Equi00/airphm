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

    ownerId: int
    baseCost: int
    name: str
    description: str
    capacity: int
    bedrooms: int
    bathrooms: int
    accommodationDetail: str
    otherAspects: str
    cleaningService: bool
    address: str
    country: str
    imageUrl: str

    reserves: List[ReserveModel] = []
    commission: float = 1.05
    rateAverage: float = 0.0
    rateCount: int = 0

    @abstractmethod
    def plus(self) -> int:
        pass

    def total_cost(self) -> int:
        return ceil((self.baseCost + self.plus()) * self.commission)

    def has_overlapped_reserves(self) -> bool:
        if len(self.reserves) <= 1:
            return False

        for reserve in self.reserves:
            remaining = [r for r in self.reserves if r != reserve]
            if reserve.overlaps(remaining):
                return True
        return False

    def is_valid(self) -> bool:
        return (
            self.baseCost > 0
            and self.name.strip()
            and self.description.strip()
            and self.capacity > 0
            and self.bedrooms > 0
            and self.bathrooms > 0
            and self.accommodationDetail.strip()
            and self.otherAspects.strip()
            and self.address.strip()
            and self.country.strip()
            and self.imageUrl.strip()
            and not self.has_overlapped_reserves()
        )
    
    def to_detail_dto(self, rates: list[RateData]) -> AccommodationDetailModel:
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
            rate=[
                RateDataCommentModel(
                    rate_score=rate.rate_score,
                    commentary=rate.commentary,
                    user=rate.user_id,
                    date=rate.date
                )
                for rate in rates
            ],
            rate_average=self.rate_average,
            rate_count=self.rate_count,
            commission=self.commission,
            type=self.__class__.__name__
        )
    
class Hut(Accommodation):
    type: Literal["Hut"] = "Hut"

    def plus(self) -> int:
        return 10000 if self.cleaningService else 0
    
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