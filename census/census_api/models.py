from django.contrib.gis.db import models


class Blockgroup(models.Model):
    state_fips_code = models.CharField('State FIPS Code', max_length='2')
    county_identifier = models.CharField(max_length=5)
    geoid = models.CharField(max_length=12,primary_key=True)
    geoid12 = models.CharField(max_length=12)
    geom = models.MultiPolygonField()
    objects = models.GeoManager()
    total_population = models.IntegerField(default=-1)
    median_household_income = models.IntegerField(default=-1)

    def __unicode__(self):
        return self.geoid
    
    def natural_key(self):
        return self.geoid
    
    class Meta:
        ordering = ['geoid']

class Neighborhood(models.Model):
    state = models.CharField(max_length=50)
    county = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    id = models.FloatField(primary_key=True)
    geom = models.MultiPolygonField()
    
    objects = models.GeoManager()
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Metro_area(models.Model):
    name = models.CharField(max_length=50)
    geoid = models.CharField(max_length=5,primary_key=True)
    geom = models.MultiPolygonField()
    
    objects = models.GeoManager()
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Water(models.Model):
    facc_code = models.CharField(max_length=5)
    cell = models.CharField(max_length=6)
    wb = models.IntegerField(default=-1)
    geom = models.MultiPolygonField()
    
    objects = models.GeoManager()
    
    def __unicode__(self):
        return self.cell
    
    class Meta:
        ordering = ['cell']

class HousingUnits(models.Model):
    geoid = models.CharField(max_length=15,primary_key=True) # 12 for blockgroups, 15 for tracts
    total = models.IntegerField(default=-1)
    vacant = models.IntegerField(default=-1)
    occupied = models.IntegerField(default=-1)
    owner_occupied = models.IntegerField(default=-1) # ACS13_5yr_B25003002
    renter_occupied = models.IntegerField(default=-1) # ACS13_5yr_B25003003
    
    def __unicode__(self):
	   return self.geoid
    
    def natural_key(self):
	   return self.geoid
    
    class Meta:
	   ordering = ['geoid']




