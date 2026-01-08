from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional
import json
from models.accommodationModel import AccommodationCacheModel


@dataclass
class AccommodationSearchCache:
    date_from: Optional[date]
    date_to: Optional[date]
    country: Optional[str]
    passengers: Optional[int]
    min_rate: Optional[int]

    accommodations: List[AccommodationCacheModel] = field(default_factory=list)
    ttl: int = 60

    @property
    def id(self) -> str:
        return self._generate_cache_key()

    def _generate_cache_key(self) -> str:
        return f"accommodations_{self.date_from}_{self.date_to}_{self.country}_{self.passengers}_{self.min_rate}"
        
    def to_redis_value(self) -> str:
        return json.dumps([
            accommodation.model_dump()
            for accommodation in self.accommodations
        ])
