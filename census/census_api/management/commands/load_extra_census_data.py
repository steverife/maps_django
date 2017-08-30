import datetime
import os
import sys
from optparse import make_option
import csv
import glob

from django.core.management.base import BaseCommand
from django.conf import settings



'''
    from django.contrib.gis.utils import LayerMapping
'''



from census_api.models import HousingUnits


def blockgroup_import(blockgroup_shp):
    blockgroup_mapping = {
        'state_fips_code': 'STATEFP',
        'county_identifier': 'COUNTYFP',
        'geoid': 'GEOID',
        'geom': 'POLYGON',
    }

    lm = LayerMapping(Blockgroup, blockgroup_shp, blockgroup_mapping)
    lm.save(verbose=True)

def blockgroup_income_import(blockgroup_data):
    #used_data = {'SE_T001_001': 'Total Population', 'SE_T057_001': 'Median Household Income (In <DollarYear> Inflation Adjusted Dollars)'}
    blockgroup_mapping = {
        'geoid': 'Geo_FIPS',
        'total_population': 'SE_T001_001',
        'median_household_income': 'SE_T057_001',
    }
    with open(blockgroup_data) as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=',')
        for row in csvreader:
            if row.has_key(blockgroup_mapping['geoid']):
               geoid = row[blockgroup_mapping['geoid']]
               print geoid
               total_population=  row[blockgroup_mapping['total_population']]
               median_household_income = row[blockgroup_mapping['median_household_income']]
               print total_population, median_household_income
               try:
                  blockgroup = Blockgroup.objects.get(geoid=geoid)
                  if blockgroup:
                     if total_population: blockgroup.total_population = total_population
                     if median_household_income: blockgroup.median_household_income = median_household_income
                     blockgroup.save()
               except:
                   print geoid, 'error'

def blockgroup_housing_import(blockgroup_data):
    #used_data = {'SE_T095_001':'Occupancy Status: Total Units',	'SE_T095_002': 'Occupancy Status: Vacant Units',	'SE_T095_003': 'SE_T142_001', 'Owner Occupied Housing Units'}


    blockgroup_mapping = {
	   'geoid': 'Geo_FIPS',
	   'total': 'SE_T095_001',
	   'occupied': 'SE_T095_002',
	   'vacant': 'SE_T095_003',
	   'owner_occupied': 'SE_T142_001'
    }



    with open(blockgroup_data) as csvfile:
	   print 'loading data'
	   csvreader = csv.DictReader(csvfile, delimiter=',')
	   for row in csvreader:
			 if row.has_key(blockgroup_mapping['geoid']):
				geoid = row[blockgroup_mapping['geoid']]
				print geoid
				total=  row[blockgroup_mapping['total']]
				occupied = row[blockgroup_mapping['occupied']]
				vacant = row[blockgroup_mapping['vacant']]
				owner_occupied = row[blockgroup_mapping['owner_occupied']]
				renter_occupied = int(occupied) - int(owner_occupied)
				housingunits = HousingUnits(geoid=geoid)
				if total: housingunits.total = total
				if occupied: housingunits.occupied = occupied
				if vacant: housingunits.vacant = vacant
				if owner_occupied: housingunits.owner_occupied = owner_occupied
				if renter_occupied: housingunits.renter_occupied = renter_occupied
				housingunits.save()


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--state', default='MA', dest='state',
            help='The two letter state abbreviation.'),
 
    )
    help = 'Installs the 2013 census_api files for blockgroups and 2013 ACS data'

    def handle(self, *args, **kwargs):
        state = kwargs['state']

        # With DEBUG on this will DIE.
        settings.DEBUG = False

        path = glob.glob('./data/census/bg_shapes/'+state+'/tl_2013_*_bg.shp')[0]
        path_income = './data/census/R10941258_SL150.csv'
        path_occupancy = './data/census/R11008227_SL150.csv'
	   #print("Blockgroup Start: %s" % datetime.datetime.now())
	   #print("Blockgroup shapes")
        #blockgroup_import(path)
	   #print("Blockgroup census data")
	   #blockgroup_income_import(path_income)
        blockgroup_housing_import(path_occupancy)
        print("End blockgroup: %s" % datetime.datetime.now())
