from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom
from graphs.accommodationGraph import AccommodationGraph

class UserGraph(StructuredNode):
    id = StringProperty(unique_index=True, required=True)

    friends = RelationshipTo("UserGraph","FRIEND_OF")

    reserves = RelationshipFrom(AccommodationGraph,"RESERVED_BY")