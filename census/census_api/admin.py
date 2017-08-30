from django.contrib.gis import admin

from census_api.models import Zipcode, State, County, Blockgroup


class ZipcodeAdmin(admin.OSMGeoAdmin):
    list_display = ('code',)
    search_fields = ('code',)


class StateAdmin(admin.OSMGeoAdmin):
    list_display = ('name', 'usps_code', 'fips_code', 'area_description_code', 'feature_class_code', 'functional_status')


class CountyAdmin(admin.OSMGeoAdmin):
    list_display = ('name', 'county_identifier', 'legal_statistical_description', 'fips_55_class_code', 'feature_class_code', 'functional_status')
    search_fields = ('name', 'state_fips_code')

class BlockgroupAdmin(admin.OSMGeoAdmin):
    list_display = ('state_fips_code','county_identifier','geoid')
    search_fields = ('geoid',)

admin.site.register(Zipcode, ZipcodeAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(County, CountyAdmin)
admin.site.register(Blockgroup, BlockgroupAdmin)