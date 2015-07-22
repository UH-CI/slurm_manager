# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClusterJobs',
            fields=[
                ('date', models.DateField(serialize=False, primary_key=True)),
                ('completed', models.IntegerField()),
                ('failed', models.IntegerField()),
                ('cancelled', models.IntegerField()),
                ('total', models.IntegerField()),
            ],
            options={
                'db_table': 'slurm_cluster_jobs',
                'managed': True,
            },
        ),
    ]
