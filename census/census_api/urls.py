# Import django modules
from django.conf.urls import include, url
from django.views.decorators.cache import cache_page

from . import views

SHORT_TIMEOUT = 60*10
LONG_TIMEOUT =  60*10

urlpatterns =[
 # Examples:
 # url(r'^$', 'views.home', name='home'),
 url(r'^$', 'census_api.views.index', name='index'),
 url(r'^blockgroup/(?P<geoid>[0-9]{12})/$', 'census_api.views.blockgroup'),
 url(r'^neighborhood/(?P<geoid>[0-9]{12})/$', 'census_api.views.neighborhood'),
 #url(r'^blockgroups/(?P<city_name>[a-z_]*).geojson$',  'census_api.views.blockgroups_geojson'),
 url(r'^blockgroups/(?P<city_name>[a-z_]*).geojson$',  cache_page(LONG_TIMEOUT)(views.blockgroups_geojson)),
 #url(r'^nhoods/(?P<city_name>[a-z_]*).geojson$', 'census_api.views.nhoods_blockgroups_geojson'),
 url(r'^nhoods/(?P<city_name>[a-z_]*).geojson$', cache_page(LONG_TIMEOUT)(views.nhoods_blockgroups_geojson)),
 #url(r'^geoid_neighbor_hash/(?P<city_name>[a-z_]*).json$', 'census_api.views.geoid_neighbor_hash'),
 url(r'^geoid_neighbor_hash/(?P<city_name>[a-z_]*).json$', cache_page(SHORT_TIMEOUT)(views.geoid_neighbor_hash)),
 #url(r'^income/(?P<city_name>[a-z_]*).csv$', 'census_api.views.income_csv'),
 url(r'^income/(?P<city_name>[a-z_]*).csv$', cache_page(SHORT_TIMEOUT)(views.income_csv)),
 #url(r'^overlap/(?P<city_name>[a-z_]*).csv$', 'census_api.views.overlap_csv'),
 url(r'^overlap/(?P<city_name>[a-z_]*).csv$', cache_page(SHORT_TIMEOUT)(views.overlap_csv)),
 #url(r'^proximity_disparity/(?P<city_name>[a-z_]*)/$', 'census_api.views.proximity_disparity'),
 url(r'^proximity_disparity/(?P<city_name>[a-z_]*)/$', cache_page(SHORT_TIMEOUT)(views.proximity_disparity)),
 url(r'^water/(?P<city_name>[a-z_]*).geojson$',  'census_api.views.water_geojson'),

              
 ]



