from neomodel import StructuredNode, StringProperty, IntegerProperty, FloatProperty, UniqueIdProperty
from entities.accommodation import Accommodation

class AccommodationGraph(StructuredNode):
    id = UniqueIdProperty()

    accommodation_id = StringProperty(required=True, unique_index=True)

    image_url = StringProperty(required=True)
    name = StringProperty(required=True)
    description = StringProperty(required=True)

    base_cost = IntegerProperty()
    capacity = IntegerProperty()

    address = StringProperty(required=True)
    country = StringProperty(required=True)

    rate_average = FloatProperty()
    rate_count = IntegerProperty()

    type = StringProperty(required=True)

    def from_accommodation(self, accommodation: Accommodation, type_: str) -> "AccommodationGraph":
        self.accommodation_id = accommodation.id
        self.image_url = accommodation.image_url
        self.name = accommodation.name
        self.description = accommodation.description
        self.base_cost = accommodation.base_cost
        self.capacity = accommodation.capacity
        self.address = accommodation.address
        self.country = accommodation.country
        self.rate_average = accommodation.rate_average
        self.rate_count = accommodation.rate_count
        self.type = type_
        return self