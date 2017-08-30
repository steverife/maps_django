# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blockgroup',
            fields=[
                ('state_fips_code', models.CharField(max_length=b'2', verbose_name=b'State FIPS Code')),
                ('county_identifier', models.CharField(max_length=5)),
                ('geoid', models.CharField(max_length=12, serialize=False, primary_key=True)),
                ('geoid12', models.CharField(max_length=12)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('total_population', models.IntegerField(default=-1)),
                ('median_household_income', models.IntegerField(default=-1)),
            ],
            options={
                'ordering': ['geoid'],
            },
        ),
        migrations.CreateModel(
            name='County',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state_fips_code', models.CharField(max_length=b'2', verbose_name=b'State FIPS Code')),
                ('fips_code', models.CharField(max_length=3, verbose_name=b'FIPS Code')),
                ('county_identifier', models.CharField(max_length=5)),
                ('name', models.CharField(max_length=100)),
                ('name_and_description', models.CharField(max_length=100)),
                ('legal_statistical_description', models.CharField(max_length=2)),
                ('fips_55_class_code', models.CharField(max_length=2)),
                ('feature_class_code', models.CharField(max_length=5)),
                ('functional_status', models.CharField(max_length=1)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
                'verbose_name_plural': 'Counties',
            },
        ),
        migrations.CreateModel(
            name='Metro_area',
            fields=[
                ('name', models.CharField(max_length=50)),
                ('geoid', models.CharField(max_length=5, serialize=False, primary_key=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Neighborhood',
            fields=[
                ('state', models.CharField(max_length=50)),
                ('county', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
                ('id', models.FloatField(serialize=False, primary_key=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='OccupiedHousingUnits',
            fields=[
                ('geoid', models.CharField(max_length=15, serialize=False, primary_key=True)),
                ('total', models.IntegerField(default=-1)),
                ('owner_occupied', models.IntegerField(default=-1)),
                ('renter_occupied', models.IntegerField(default=-1)),
            ],
            options={
                'ordering': ['geoid'],
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fips_code', models.CharField(max_length=2, verbose_name=b'FIPS Code')),
                ('usps_code', models.CharField(max_length=2, verbose_name=b'USPS state abbreviation', db_index=True)),
                ('name', models.CharField(max_length=100, db_index=True)),
                ('area_description_code', models.CharField(max_length=2)),
                ('feature_class_code', models.CharField(max_length=5)),
                ('functional_status', models.CharField(max_length=1)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Water',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('facc_code', models.CharField(max_length=5)),
                ('cell', models.CharField(max_length=6)),
                ('wb', models.IntegerField(default=-1)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
                'ordering': ['cell'],
            },
        ),
        migrations.CreateModel(
            name='Zipcode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=5, db_index=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            options={
                'ordering': ['code'],
            },
        ),
    ]
