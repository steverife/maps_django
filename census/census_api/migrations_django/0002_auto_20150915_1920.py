# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('census_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HousingUnits',
            fields=[
                ('geoid', models.CharField(max_length=15, serialize=False, primary_key=True)),
                ('total', models.IntegerField(default=-1)),
                ('vacant', models.IntegerField(default=-1)),
                ('occupied', models.IntegerField(default=-1)),
                ('owner_occupied', models.IntegerField(default=-1)),
                ('renter_occupied', models.IntegerField(default=-1)),
            ],
            options={
                'ordering': ['geoid'],
            },
        ),
        migrations.DeleteModel(
            name='OccupiedHousingUnits',
        ),
    ]
