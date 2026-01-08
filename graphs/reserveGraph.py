from neomodel import StructuredRel, DateProperty

class ReserveGraph(StructuredRel):
    start_date = DateProperty(required=True)