
import csv
from django.http import HttpResponse
import logging
from models import Blockgroup, Neighborhood, HousingUnits
from django.contrib.gis.geos import Polygon
from operator import itemgetter
logger = logging.getLogger(__name__)


def getBoundsCity(city_name):
    city_dict={'boston':{'states':['MA'],'cities':['Boston', 'Cambridge']},
        'springfield_ma':{'states':['MA'],'cities':['Springfield']},
        'baltimore':{'states':['MD'],'cities':['Baltimore']},
        'washington':{'states':['DC'],'cities':['Washington']},
        'philadelphia':{'states':['PA'],'cities':['Philadelphia']},
        'pittsburgh':{'states':['PA'],'cities':['Pittsburgh']},
        'phoenix':{'states':['AZ'],'cities':['Phoenix', 'Mesa','Tempe','Scottsdale']},
        'houston':{'states':['TX'],'cities':['Houston']},
        'austin':{'states':['TX'],'cities':['Austin']},
        'dallas':{'states':['TX'],'cities':['Dallas','Fort Worth','Arlington']},
        'el_paso':{'states':['TX'],'cities':['El Paso']},
        'san_antonio':{'states':['TX'],'cities':['San Antonio']},
        'san_diego':{'states':['CA'],'cities':['San Diego']},
        'san_francisco':{'states':['CA'],'cities':['San Francisco','Oakland']},
        'los_angeles':{'states':['CA'],'cities':['Los Angeles']},
        'sacramento':{'states':['CA'],'cities':['Sacramento']},
        'san_jose':{'states':['CA'],'cities':['San Jose']},
        'memphis':{'states':['TN'],'cities':['Memphis']},
        'nashville':{'states':['TN'],'cities':['Nashville']},
        #'indianapolis':{'states':['IN'],'cities':['Indianapolis']},
        'jacksonville':{'states':['FL'],'cities':['Jacksonville']},
        'miami':{'states':['FL'],'cities':['Miami']},
        'cincinnati':{'states':['OH'],'cities':['Cincinnati']},
        'akron':{'states':['OH'],'cities':['Akron']},
        'columbus_oh':{'states':['OH'],'cities':['Columbus']},
        'dayton':{'states':['OH'],'cities':['Dayton']},
        'toledo':{'states':['OH'],'cities':['Toledo']},
        'charlotte':{'states':['NC'],'cities':['Charlotte']},
        'raleigh':{'states':['NC'],'cities':['Raleigh']},
        'denver':{'states':['CO'],'cities':['Denver','Aurora']},
        'colorado_springs':{'states':['CO'],'cities':['Colorado Springs']},
        'seattle':{'states':['WA'],'cities':['Seattle']},
        'detroit':{'states':['MI'],'cities':['Detroit']},
        'honolulu':{'states':['HI'],'cities':['Honolulu']},
        'fort_worth':{'states':['TX'],'cities':['Fort Worth']},
        'louisville':{'states':['KY'],'cities':['Louisville']},
        'lexington':{'states':['KY'],'cities':['Lexington']},
        'portland':{'states':['OR'],'cities':['Portland','Beaverton','Milwaukie',]},
        'salem':{'states':['OR'],'cities':['Salem']},
        'eugene':{'states':['OR'],'cities':['Eugene']},
        'las_vegas':{'states':['NV'],'cities':['Las Vegas','North Las Vegas','Henderson',]},
        'reno':{'states':['NV'],'cities':['Reno']},
        'milwaukee':{'states':['WI'],'cities':['Milwaukee']},
        'madison':{'states':['WI'],'cities':['Madison']},
        'albuquerque':{'states':['NM'],'cities':['Albuquerque']},
        'fresno':{'states':['CA'],'cities':['Fresno']},
        'kansas_city':{'states':['MO'],'cities':['Kansas City']},
        'saint_louis':{'states':['MO'],'cities':['Saint Louis']},
        'tucson':{'states':['AZ'],'cities':['Tucson']},
        'minneapolis':{'states':['MN'],'cities':['Minneapolis','Saint Paul']},
        'oakland':{'states':['CA'],'cities':['Oakland']},
        'wichita':{'states':['KS'],'cities':['Wichita']},
        'new_orleans':{'states':['LA'],'cities':['New Orleans']},
        'shreveport':{'states':['LA'],'cities':['Shreveport']},
        #
        #'omaha':{'states':['NE'],'cities':['Omaha']},
        #'tulsa':{'states':['OK'],'cities':['Tulsa']},
        'bakersfield':{'states':['CA'],'cities':['Bakersfield']},
        'tampa':{'states':['FL'],'cities':['Tampa']},
        'corpus_christi':{'states':['TX'],'cities':['Corpus Christi']},
        'stockton':{'states':['CA'],'cities':['Stockton']},
        'newark':{'states':['NJ'],'cities':['Newark']},
        'salt_lake_city':{'states':['UT'],'cities':['Salt Lake City']},
        'albany':{'states':['NY'],'cities':['Albany']},
        'buffalo':{'states':['NY'],'cities':['Buffalo']},
        'albany':{'states':['NY'],'cities':['Albany']},
        'rochester':{'states':['NY'],'cities':['Rochester']},
        'syracuse':{'states':['NY'],'cities':['Syracuse']},
        'jersey_city':{'states':['NJ'],'cities':['Jersey City']},
        'trenton':{'states':['NJ'],'cities':['Trenton']},
        'newark':{'states':['NJ'],'cities':['Newark']},
        'boulder':{'states':['CO'],'cities':['Boulder']},
        'anchorage':{'states':['AK'],'cities':['Anchorage']},
        'little_rock':{'states':['AR'],'cities':['Little Rock']},
        'mobile':{'states':['AL'],'cities':['Mobile']},
        'hartford':{'states':['CT'],'cities':['Hartford']},
        'new_haven':{'states':['CT'],'cities':['New Haven']},
        'orlando':{'states':['FL'],'cities':['Orlando']},
        'fort_lauderdale':{'states':['FL'],'cities':['Fort Lauderdale']},
        'augusta':{'states':['GA'],'cities':['Augusta']},
        'des_moines':{'states':['IA'],'cities':['Des Moines']},
        'boise':{'states':['ID'],'cities':['Boise']},
        'fort_wayne':{'states':['IN'],'cities':['Fort Wayne']},
        'portland_me':{'states':['ME'],'cities':['Portland']},
        'jackson':{'states':['MS'],'cities':['Jackson']},
        'providence':{'states':['RI'],'cities':['Providence']},
        'knoxville':{'states':['TN'],'cities':['Knoxville']},
        'richmond':{'states':['VA'],'cities':['Richmond']},
        'charlottesville':{'states':['VA'],'cities':['Charlottesville']},
        'chesapeake':{'states':['VA'],'cities':['Chesapeake']},
        'spokane':{'states':['WA'],'cities':['Spokane']},
        'tacoma':{'states':['WA'],'cities':['Tacoma']},
        'grand_rapids':{'states':['MI'],'cities':['Grand Rapids']},
}

    if city_dict.has_key(city_name):
        city_info= city_dict[city_name]
        nhoods = Neighborhood.objects.filter(state__in=city_info['states']).filter(city__in=city_info['cities'])
        bounds = (min(nhoods,key=lambda item:item.geom.extent[0]).geom.extent[0],
              min(nhoods,key=lambda item:item.geom.extent[1]).geom.extent[1],
              max(nhoods,key=lambda item:item.geom.extent[2]).geom.extent[2],
              max(nhoods,key=lambda item:item.geom.extent[3]).geom.extent[3])
        return bounds
    else:
        return (0,0,0,0)

def polygonFromBounds(bounds):
    return Polygon( ((bounds[0], bounds[1]), (bounds[0], bounds[3]),(bounds[2], bounds[3]),(bounds[2], bounds[1]),(bounds[0], bounds[1]) ) )

def getPolygonFromCity(city_name):
    return polygonFromBounds(getBoundsCity(city_name))

def create_nhood_blockgroup_data(blockgroup_shapes,nhood_shapes):
   nhood_blockgroups = {}
   blockgroup_nhoods = {}
   for blockgroup in blockgroup_shapes:
      blockgroup_nhoods[blockgroup.geoid] = []

   for nhood in nhood_shapes:
      nhood_blockgroups[nhood.name] = []
      for blockgroup in blockgroup_shapes:
         try:
            intersection = blockgroup.geom.intersection(nhood.geom)
         except:
             try:
                intersection = blockgroup_shape.intersection(nhood.geom.convex_hull)
             except:
                intersection = None
                logger.debug(str(blockgroup.geoid)+' error in create_nhood_blockgroup_data finding intersection')
         if (intersection) and (intersection.area/ blockgroup.geom.area > 0.5):
            nhood_blockgroups[nhood.name].append([blockgroup.geoid, intersection.area/ blockgroup.geom.area])
            blockgroup_nhoods[blockgroup.geoid].append(nhood.name)
   return(nhood_blockgroups,blockgroup_nhoods)

import csv

def create_income_csv(request,blockgroup_shapes):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=city_name+"_income.csv"'
    writer = csv.writer(response,delimiter=',')
    writer.writerow(['Id','Median','Total'])
    for blockgroup in blockgroup_shapes:
        writer.writerow([blockgroup.geoid,blockgroup.median_household_income,blockgroup.total_population])
    return response

def create_occupancy_csv(request,blockgroup_shapes):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=city_name+"_occupancy.csv"'
    writer = csv.writer(response,delimiter=',')
    writer.writerow(['Id','total','occupied'])
    for blockgroup in blockgroup_shapes:
	   units= HousingUnits.objects.filter(geoid=geoid)
	   if units:
		  units_data = units[0]
		  writer.writerow([blockgroup.geoid,units_data.total,units_data.occupied])
    return response

def create_overlap_csv(request,blockgroups):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=city_name+"_overlap.csv"'
    writer = csv.writer(response,delimiter=',')
    intersections = create_intersections(blockgroups)
    overlap_lines_to_csv(writer, intersections)
    return response

'''def create_intersections(blockgroups):
    intersections = []
    for counter1 in range(len(blockgroups)):
        bg1 = blockgroups[counter1]
        for counter2 in range(counter1,len(blockgroups)):
            bg2 = blockgroups[counter2]
            intersection = bg1.geom.intersection(bg2.geom)
            if intersection:
                intersections.append((intersection,(bg1.geoid,bg2.geoid)))
    return intersections
'''

def create_intersections(blockgroups):
    intersections = []
    for bg in blockgroups:
        bg_intersections = Blockgroup.objects.filter(geom__touches=bg.geom)
        if bg_intersections:
            for bgi in bg_intersections:
                if bgi.geoid != bg.geoid:
                   intersection = bgi.geom.intersection(bg.geom)
                   intersections.append((intersection,(bg.geoid,bgi.geoid)))
    return intersections

def overlap_lines_to_csv(writer, intersections):
    rows = []
    for intersection in intersections:
        intersection_geo = intersection[0]
        # print intersection_geo['type']
        if intersection_geo.geom_type == 'MultiLineString':
            coords = intersection_geo.coords
            unzipped_list = zip(*coords)
            coord_list1= unzipped_list[0]
            coord_list2= unzipped_list[1]
            for counter in range(len(coord_list1)):
                rows.append([coord_list1[counter][0],coord_list1[counter][1],coord_list2[counter][0],coord_list2[counter][1],intersection[1][0],intersection[1][1]])
        elif intersection_geo.geom_type == 'LineString':
            coords = intersection_geo.coords
            rows.append([coords[0][0],coords[0][1],coords[1][0],coords[1][1],intersection[1][0],intersection[1][1]])
        elif intersection_geo.geom_type == 'Point':
            coords = intersection_geo.coords
            rows.append([coords[0],coords[1],'','',intersection[1][0],intersection[1][1]])
        elif intersection_geo.geom_type == 'MultiPoint':
            coords = intersection_geo.coords
            for pair in coords:
                rows.append([pair[0],pair[1],'','',intersection[1][0],intersection[1][1]])
        elif intersection_geo.geom_type == 'GeometryCollection':
            for geo in intersection_geo:
                if geo.geom_type == 'MultiLineString':
                    coords = geo.coords
                    unzipped_list = zip(*coords)
                    coord_list1= unzipped_list[0]
                    coord_list2= unzipped_list[1]
                    for counter in range(len(coord_list1)):
                        rows.append([coord_list1[counter][0],coord_list1[counter][1],coord_list2[counter][0],coord_list2[counter][1],intersection[1][0],intersection[1][1]])
                elif geo.geom_type == 'LineString':
                    coords = geo.coords
                    rows.append([coords[0][0],coords[0][1],coords[1][0],coords[1][1],intersection[1][0],intersection[1][1]])
                elif geo.geom_type == 'Point':
                    coords = geo.coords
                    rows.append([coords[0],coords[1],'','',intersection[1][0],intersection[1][1]])
        else:
            pass
    writer.writerow(['lng1','lat1','lng2','lat2','id1','id2'])
    for row in rows:
       writer.writerow(row)
    return writer

