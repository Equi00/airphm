from pydantic import BaseModel
from typing import List, Optional

from models.rateDataModel import RateDataCommentModel
from models.reserveModel import ReserveModel


class AccommodationDetailModel(BaseModel):
    id: str
    owner_id: Optional[int]
    name: str
    description: str
    base_cost: int
    capacity: int
    bedrooms: int
    bathrooms: int
    accommodation_detail: str
    other_aspects: str
    cleaning_service: bool
    address: str
    country: str
    image_url: str
    reserves: List[ReserveModel]
    rates: List[RateDataCommentModel]
    rate_average: float
    rate_count: int
    commission: float
    type: str

class AccommodationCacheModel(BaseModel):
    id: str 
    name: str 
    description: str 
    base_cost: int 
    capacity: int 
    address: str 
    country: str 
    image_url: str 
    rate_average: float 
    rate_count: int 
    type: str 