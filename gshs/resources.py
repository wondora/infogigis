from import_export import resources
from gshs.models import Infogigi, Place, People

class InfogigiResource(resources.ModelResource):
    class Meta:
        model = Infogigi

class PeopleResource(resources.ModelResource):
    class Meta:
        model = People

class PlaceResource(resources.ModelResource):
    class Meta:
        model = Place