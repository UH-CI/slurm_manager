# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slurm_manager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClusterTime',
            fields=[
                ('date', models.DateField(serialize=False, primary_key=True)),
                ('time_used', models.BigIntegerField()),
            ],
            options={
                'db_table': 'cluster_time',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='UohJobTable',
            fields=[
                ('job_db_inx', models.AutoField(serialize=False, primary_key=True)),
                ('mod_time', models.IntegerField()),
                ('deleted', models.IntegerField()),
                ('account', models.TextField(null=True, blank=True)),
                ('cpus_req', models.IntegerField()),
                ('cpus_alloc', models.IntegerField()),
                ('derived_ec', models.IntegerField()),
                ('derived_es', models.TextField(null=True, blank=True)),
                ('exit_code', models.IntegerField()),
                ('job_name', models.TextField()),
                ('id_assoc', models.IntegerField()),
                ('id_block', models.TextField(null=True, blank=True)),
                ('id_job', models.IntegerField()),
                ('id_qos', models.IntegerField()),
                ('id_resv', models.IntegerField()),
                ('id_wckey', models.IntegerField()),
                ('id_user', models.IntegerField()),
                ('id_group', models.IntegerField()),
                ('kill_requid', models.IntegerField()),
                ('mem_req', models.IntegerField()),
                ('nodelist', models.TextField(null=True, blank=True)),
                ('nodes_alloc', models.IntegerField()),
                ('node_inx', models.TextField(null=True, blank=True)),
                ('partition', models.TextField()),
                ('priority', models.IntegerField()),
                ('state', models.SmallIntegerField()),
                ('timelimit', models.IntegerField()),
                ('time_submit', models.IntegerField()),
                ('time_eligible', models.IntegerField()),
                ('time_start', models.IntegerField()),
                ('time_end', models.IntegerField()),
                ('time_suspended', models.IntegerField()),
                ('gres_req', models.TextField()),
                ('gres_alloc', models.TextField()),
                ('gres_used', models.TextField()),
                ('wckey', models.TextField()),
                ('track_steps', models.IntegerField()),
            ],
            options={
                'db_table': 'uoh_job_table',
                'managed': True,
            },
        ),
        migrations.AlterUniqueTogether(
            name='uohjobtable',
            unique_together=set([('id_job', 'id_assoc', 'time_submit')]),
        ),
    ]
