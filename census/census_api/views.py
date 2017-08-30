from django.conf import settings
from django.contrib.gis.maps.google import GoogleMap
from django.contrib.gis.maps.google.overlays import GMarker, GEvent, GPolyline, GPolygon
from django.contrib.gis.geos import GeometryCollection
from django.shortcuts import get_object_or_404, render_to_response
from models import Zipcode, Blockgroup, Neighborhood, Water
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.core import serializers
from djgeojson.serializers import Serializer as GeoJSONSerializer
import json
import disparity_utils

class Bg_Serializer(GeoJSONSerializer):
    class Meta:
        model= Blockgroup
        fields = ('geoid', 'total_population','median_household_income'),
        extra_kwargs = {
                    "geoid": {
                    "read_only": False,
                    "required": False,
                            }}


def zipcode_detail(request, object_id):
    zipcode = get_object_or_404(Zipcode, code=object_id)

    polygons = ()

    polygons += (GPolygon(zipcode.geom),)

    return render_to_response('census/zipcode_detail.html', {
        'google': GoogleMap(key=settings.GOOGLE_MAPS_API_KEY, polygons=polygons),
        'object': zipcode,
    })


def index(request):
    'Display map'
    return render_to_response('census_api/index.html', {
                              })


def blockgroup(request,geoid):
    'Display map'
    bg = Blockgroup.objects.get(geoid=geoid)
    state = bg.state_fips_code
    shape = bg.geom.centroid
    lat= shape.y
    lon= shape.x
    result= Blockgroup.objects.raw("SELECT b.geoid FROM census_api_blockgroup as a JOIN census_api_blockgroup as b ON ST_Touches((SELECT a.geom FROM census_api_blockgroup as a WHERE a.geoid = '"+geoid+"'),b.geom);")
    return render_to_response('census_api/blockgroup.html', {'geoid':geoid, 'state':result[0], 'lat': lat, 'lon': lon
                              })


def neighborhood1(request,geoid):
    bg = Blockgroup.objects.get(geoid=geoid)
    state = bg.state_fips_code
    shape = bg.geom.centroid
    lat= shape.y
    lon= shape.x
    nhood = Neighborhood.objects.filter(geom__intersects=shape)
    name = ''
    if nhood:
       name = nhood[0].name
    return render_to_response('census_api/blockgroup.html', {'geoid':geoid, 'state':name, 'lat': lat, 'lon': lon
                              })

def neighborhood(request,geoid):
    some_data_to_dump = {
        'some_var_1': 'foo',
        'some_var_2': 'bar',}
    data = json.dumps(some_data_to_dump)
    return HttpResponse(data, content_type='application/json')

def blockgroups_geojson(request,city_name):
    #bg = Blockgroup.objects.filter(state_fips_code__in=['25',],county_identifier__in=['025','017',])
    #bg_serialize = Bg_Serializer()
    bg = Blockgroup.objects.filter(geom__intersects=disparity_utils.getPolygonFromCity(city_name))
    #data = GeoJSONSerializer(bg.all(),use_natural_keys=True)
    #data = serializers.serialize('geojson',  bg.all(), use_natural_foreign_keys=True, use_natural_primary_keys=True)
    data = serializers.serialize('geojson', bg.all(), fields = ('geom', 'geoid12', 'total_population','median_household_income') )
    struct = json.loads(data)
    data = json.dumps(struct)
    return HttpResponse(data, content_type='application/json')

def income_csv(request,city_name):
    #bg = Blockgroup.objects.filter(state_fips_code__in=['25',],county_identifier__in=['025','017',])
    bg = Blockgroup.objects.filter(geom__intersects=disparity_utils.getPolygonFromCity(city_name))
    response = disparity_utils.create_income_csv(request,bg.all())
    return response

def overlap_csv(request,city_name):
    #bg = Blockgroup.objects.filter(state_fips_code__in=['25',],county_identifier__in=['025','017',])
    bg = Blockgroup.objects.filter(geom__intersects=disparity_utils.getPolygonFromCity(city_name))
    response = disparity_utils.create_overlap_csv(request,bg.all())
    return response

def occupancy_csv(request,city_name):
    bg = Blockgroup.objects.filter(geom__intersects=disparity_utils.getPolygonFromCity(city_name))
    response = disparity_utils.create_occupancy_csv(request,bg.all())
    return response

def nhoods_blockgroups_geojson(request,city_name):
    #bg = Blockgroup.objects.filter(state_fips_code__in=['25',],county_identifier__in=['025','017',])
    bg = Blockgroup.objects.filter(geom__intersects=disparity_utils.getPolygonFromCity(city_name))
    polys = []
    for group in bg.all():
       polys.append(group.geom)
    data = GeometryCollection(polys).envelope
    nhoods = Neighborhood.objects.filter(geom__intersects=data)
    blockgroups = bg.all()
    nhood_blockgroups,blockgroup_nhoods = disparity_utils.create_nhood_blockgroup_data(blockgroups,nhoods)
    data = json.dumps({'nhood_blockgroups':nhood_blockgroups,'blockgroup_nhoods':blockgroup_nhoods})
    return HttpResponse(data, content_type='application/json')

def geoid_neighbor_hash(request,city_name):
    #bg = Blockgroup.objects.filter(state_fips_code__in=['25',],county_identifier__in=['025','017',])
    bg = Blockgroup.objects.filter(geom__intersects=disparity_utils.getPolygonFromCity(city_name))
    neighbor_hash ={}
    for blockgroup in bg:
       neighbor_bg = Blockgroup.objects.filter(geom__touches=blockgroup.geom)
       neighbor_hash[blockgroup.geoid] = [neighbor.geoid for neighbor in neighbor_bg]
    data = json.dumps(neighbor_hash)
    return HttpResponse(data, content_type='application/json')

def proximity_disparity(request,city_name):
    return render_to_response('census_api/100-maps/proximity_disparity.html', {'city_name':city_name})

def water_geojson(request,city_name):
    water = Water.objects.filter(geom__intersects=disparity_utils.getPolygonFromCity(city_name))
    data = serializers.serialize('geojson', water.all(), fields = ('geom'))
    struct = json.loads(data)
    data = json.dumps(struct)
    return HttpResponse(data, content_type='application/json')

