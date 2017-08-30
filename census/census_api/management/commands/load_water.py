# http://gis.ess.washington.edu/data/vector/worldshore/index.html
'''World WaterBodies
    
    This is the world surface water body dataset created by NASA in conjunction with the version2 SRTM DEM. NASA distributes the data as one-degree shapefiles. It is available here as four large shapefiles:
    shore_ne.zip 277183482 zipped bytes, 1309470028-byte shore_ne.shp, etc.
    shore_nw.zip 396255714 zipped bytes, 1809050484-byte shore_nw.shp, etc.
    shore_se.zip 86225971 zipped bytes, 382539656-byte shore_se.shp, etc.
    shore_sw.zip 96164903 zipped bytes, 589845568-byte shore_sw.shp, etc.
    
    Questions or answers? Ask Harvey Greenberg.'''


import os
import glob
from django.core.management.base import BaseCommand
from django.conf import settings

try:
    from django.contrib.gis.utils import LayerMapping
except ImportError:
    print("gdal is required")
    sys.exit(1)

from census_api.models import Water

def water_import(water_shp, name):
    blockgroup_mapping = {
        'facc_code': 'FACC_CODE',
        'cell': 'Cell',
        'wb': 'WB',
        'geom': 'POLYGON',
    }
    
    lm = LayerMapping(Blockgroup, blockgroup_shp, blockgroup_mapping)
    lm.save(verbose=True)

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--quadrant', default='nw', dest='quadrant',
        help='The two letter quadrant: ne nw sw se.'),
        )

def handle(self, *args, **kwargs):
    quadrant = kwargs['quadrant']
    # With DEBUG on this will DIE.
    settings.DEBUG = False
    path_water = 'census/data/water/shore_'+quadrant+'/shore_'+quadrant+'.shp'
    water_import(path,quadrant)