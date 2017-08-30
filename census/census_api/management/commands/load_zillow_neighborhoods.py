import datetime
import os
import sys
from optparse import make_option

from django.core.management.base import BaseCommand
from django.conf import settings

try:
    from django.contrib.gis.utils import LayerMapping
except ImportError:
    print("gdal is required")
    sys.exit(1)

from census_api.models import Neighborhood


def neighborhood_import(neighborhood_shp):
    neighborhood_mapping = {
        'state': 'STATE',
        'county': 'COUNTY',
        'city': 'CITY',
        'name': 'NAME',
        'id': 'REGIONID',
        'geom': 'POLYGON',
    }

    lm = LayerMapping(Neighborhood, neighborhood_shp, neighborhood_mapping)
    lm.save(verbose=True)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--path', default='', dest='path',
            help='The directory where the zipcode data is stored.'),
    )
    help = 'Installs the 2010/2012/2013/2014 census_api files for zipcodes'

    def handle(self, *args, **kwargs):
        path = kwargs['path']

        # With DEBUG on this will DIE.
        settings.DEBUG = False

        path = './data/neighborhoods/states/ZillowNeighborhoods-TN.shp'
        
        print("Neighborhoods Start: %s" % datetime.datetime.now())
        neighborhood_import(path)
        print("End Neighborhoods: %s" % datetime.datetime.now())
