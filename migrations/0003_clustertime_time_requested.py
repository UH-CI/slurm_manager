# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slurm_manager', '0002_auto_20150721_2035'),
    ]

    operations = [
        migrations.AddField(
            model_name='clustertime',
            name='time_requested',
            field=models.BigIntegerField(default=0),
            preserve_default=False,
        ),
    ]
