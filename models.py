# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class AcctCoordTable(models.Model):
    creation_time = models.IntegerField()
    mod_time = models.IntegerField()
    deleted = models.IntegerField(blank=True, null=True)
    acct = models.TextField()
    user = models.TextField()

    class Meta:
        managed = False
        db_table = 'acct_coord_table'
        unique_together = (('acct', 'user'),)
        app_label = 'slurm'

class AcctTable(models.Model):
    creation_time = models.IntegerField()
    mod_time = models.IntegerField()
    deleted = models.IntegerField(blank=True, null=True)
    name = models.TextField(primary_key=True)
    description = models.TextField()
    organization = models.TextField()

    class Meta:
        managed = False
        db_table = 'acct_table'
        app_label = 'slurm'

class ClusResTable(models.Model):
    creation_time = models.IntegerField()
    mod_time = models.IntegerField()
    deleted = models.IntegerField(blank=True, null=True)
    cluster = models.TextField()
    res_id = models.IntegerField()
    percent_allowed = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clus_res_table'
        unique_together = (('res_id', 'cluster'), ('res_id', 'cluster'),)
        app_label = 'slurm'

class ClusterTable(models.Model):
    creation_time = models.IntegerField()
    mod_time = models.IntegerField()
    deleted = models.IntegerField(blank=True, null=True)
    name = models.TextField(primary_key=True)
    control_host = models.TextField()
    control_port = models.IntegerField()
    last_port = models.IntegerField()
    rpc_version = models.SmallIntegerField()
    classification = models.SmallIntegerField(blank=True, null=True)
    dimensions = models.SmallIntegerField(blank=True, null=True)
    plugin_id_select = models.SmallIntegerField(blank=True, null=True)
    flags = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cluster_table'
        app_label = 'slurm'

class ProdAssocTable(models.Model):
    creation_time = models.IntegerField()
    mod_time = models.IntegerField()
    deleted = models.IntegerField()
    is_def = models.IntegerField()
    id_assoc = models.AutoField(primary_key=True)
    user = models.TextField()
    acct = models.TextField()
    partition = models.TextField()
    parent_acct = models.TextField()
    lft = models.IntegerField()
    rgt = models.IntegerField()
    shares = models.IntegerField()
    max_jobs = models.IntegerField(blank=True, null=True)
    max_submit_jobs = models.IntegerField(blank=True, null=True)
    max_cpus_pj = models.IntegerField(blank=True, null=True)
    max_nodes_pj = models.IntegerField(blank=True, null=True)
    max_wall_pj = models.IntegerField(blank=True, null=True)
    max_cpu_mins_pj = models.BigIntegerField(blank=True, null=True)
    max_cpu_run_mins = models.BigIntegerField(blank=True, null=True)
    grp_jobs = models.IntegerField(blank=True, null=True)
    grp_submit_jobs = models.IntegerField(blank=True, null=True)
    grp_cpus = models.IntegerField(blank=True, null=True)
    grp_mem = models.IntegerField(blank=True, null=True)
    grp_nodes = models.IntegerField(blank=True, null=True)
    grp_wall = models.IntegerField(blank=True, null=True)
    grp_cpu_mins = models.BigIntegerField(blank=True, null=True)
    grp_cpu_run_mins = models.BigIntegerField(blank=True, null=True)
    def_qos_id = models.IntegerField(blank=True, null=True)
    qos = models.TextField()
    delta_qos = models.TextField()

    class Meta:
        managed = False
        db_table = 'prod_assoc_table'
        unique_together = (('user', 'acct', 'partition'),)
        app_label = 'slurm'

class ProdAssocUsageDayTable(models.Model):
    creation_time = models.IntegerField()
    mod_time = models.IntegerField()
    deleted = models.IntegerField()
    id_assoc = models.IntegerField()
    time_start = models.IntegerField()
    alloc_cpu_secs = models.BigIntegerField()
    consumed_energy = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'prod_assoc_usage_day_table'
        unique_together = (('id_assoc', 'time_start'),)
        app_label = 'slurm'

class ProdAssocUsageHourTable(models.Model):
    creation_time = models.IntegerField()
    mod_time = models.IntegerField()
    deleted = models.IntegerField()
    id_assoc = models.IntegerField()
    time_start = models.IntegerField()
    alloc_cpu_secs = models.BigIntegerField()
    consumed_energy = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'prod_assoc_usage_hour_table'
        unique_together = (('id_assoc', 'time_start'),)
        app_label = 'slurm'

class ProdAssocUsageMonthTable(models.Model):
    creation_time = models.IntegerField()
    mod_time = models.IntegerField()
    deleted = models.IntegerField()
    id_assoc = models.IntegerField()
    time_start = models.IntegerField()
    alloc_cpu_secs = models.BigIntegerField()
    consumed_energy = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'prod_assoc_usage_month_table'
        unique_together = (('id_assoc', 'time_start'),)
        app_label = 'slurm'

class ProdEventTable(models.Model):
    time_start = models.IntegerField()
    time_end = models.IntegerField()
    node_name = models.TextField()
    cluster_nodes = models.TextField()
    cpu_count = models.IntegerField()
    reason = models.TextField()
    reason_uid = models.IntegerField()
    state = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'prod_event_table'
        unique_together = (('node_name', 'time_start'),)
        app_label = 'slurm'

class ProdJobTable(models.Model):
    job_db_inx = models.AutoField(primary_key=True)
    mod_time = models.IntegerField()
    deleted = models.IntegerField()
    account = models.TextField(blank=True, null=True)
    cpus_req = models.IntegerField()
    cpus_alloc = models.IntegerField()
    derived_ec = models.IntegerField()
    derived_es = models.TextField(blank=True, null=True)
    exit_code = models.IntegerField()
    job_name = models.TextField()
    id_assoc = models.IntegerField()
    id_block = models.TextField(blank=True, null=True)
    id_job = models.IntegerField()
    id_qos = models.IntegerField()
    id_resv = models.IntegerField()
    id_wckey = models.IntegerField()
    id_user = models.IntegerField()
    id_group = models.IntegerField()
    kill_requid = models.IntegerField()
    mem_req = models.IntegerField()
    nodelist = models.TextField(blank=True, null=True)
    nodes_alloc = models.IntegerField()
    node_inx = models.TextField(blank=True, null=True)
    partition = models.TextField()
    priority = models.IntegerField()
    state = models.SmallIntegerField()
    timelimit = models.IntegerField()
    time_submit = models.IntegerField()
    time_eligible = models.IntegerField()
    time_start = models.IntegerField()
    time_end = models.IntegerField()
    time_suspended = models.IntegerField()
    gres_req = models.TextField()
    gres_alloc = models.TextField()
    gres_used = models.TextField()
    wckey = models.TextField()
    track_steps = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'prod_job_table'
        unique_together = (('id_job', 'id_assoc', 'time_submit'),)
        app_label = 'slurm'

class ProdLastRanTable(models.Model):
    hourly_rollup = models.IntegerField()
    daily_rollup = models.IntegerField()
    monthly_rollup = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'prod_last_ran_table'
        app_label = 'slurm'

class ProdResvTable(models.Model):
    id_resv = models.IntegerField()
    deleted = models.IntegerField()
    assoclist = models.TextField()
    cpus = models.IntegerField()
    flags = models.SmallIntegerField()
    nodelist = models.TextField()
    node_inx = models.TextField()
    resv_name = models.TextField()
    time_start = models.IntegerField()
    time_end = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'prod_resv_table'
        unique_together = (('id_resv', 'time_start'),)
        app_label = 'slurm'

class ProdStepTable(models.Model):
    job_db_inx = models.IntegerField()
    deleted = models.IntegerField()
    cpus_alloc = models.IntegerField()
    exit_code = models.IntegerField()
    id_step = models.IntegerField()
    kill_requid = models.IntegerField()
    nodelist = models.TextField()
    nodes_alloc = models.IntegerField()
    node_inx = models.TextField(blank=True, null=True)
    state = models.SmallIntegerField()
    step_name = models.TextField()
    task_cnt = models.IntegerField()
    task_dist = models.SmallIntegerField()
    time_start = models.IntegerField()
    time_end = models.IntegerField()
    time_suspended = models.IntegerField()
    user_sec = models.IntegerField()
    user_usec = models.IntegerField()
    sys_sec = models.IntegerField()
    sys_usec = models.IntegerField()
    max_pages = models.IntegerField()
    max_pages_task = models.IntegerField()
    max_pages_node = models.IntegerField()
    ave_pages = models.FloatField()
    max_rss = models.BigIntegerField()
    max_rss_task = models.IntegerField()
    max_rss_node = models.IntegerField()
    ave_rss = models.FloatField()
    max_vsize = models.BigIntegerField()
    max_vsize_task = models.IntegerField()
    max_vsize_node = models.IntegerField()
    ave_vsize = models.FloatField()
    min_cpu = models.IntegerField()
    min_cpu_task = models.IntegerField()
    min_cpu_node = models.IntegerField()
    ave_cpu = models.FloatField()
    act_cpufreq = models.FloatField()
    consumed_energy = models.FloatField()
    req_cpufreq = models.IntegerField()
    max_disk_read = models.FloatField()
    max_disk_read_task = models.IntegerField()
    max_disk_read_node = models.IntegerField()
    ave_disk_read = models.FloatField()
    max_disk_write = models.FloatField()
    max_disk_write_task = models.IntegerField()
    max_disk_write_node = models.IntegerField()
    ave_disk_write = models.FloatField()

    class Meta:
        managed = False
        db_table = 'prod_step_table'
        unique_together = (('job_db_inx', 'id_step'),)
        app_label = 'slurm'

class ProdSuspendTable(models.Model):
    job_db_inx = models.IntegerField()
    id_assoc = models.IntegerField()
    time_start = models.IntegerField()
    time_end = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'prod_suspend_table'
        app_label = 'slurm'

class ProdUsageDayTable(models.Model):
    creation_time = models.IntegerField()
    mod_time = models.IntegerField()
    deleted = models.IntegerField()
    time_start = models.IntegerField(primary_key=True)
    cpu_count = models.IntegerField()
    alloc_cpu_secs = models.BigIntegerField()
    down_cpu_secs = models.BigIntegerField()
    pdown_cpu_secs = models.BigIntegerField()
    idle_cpu_secs = models.BigIntegerField()
    resv_cpu_secs = models.BigIntegerField()
    over_cpu_secs = models.BigIntegerField()
    consumed_energy = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'prod_usage_day_table'
        app_label = 'slurm'

class ProdUsageHourTable(models.Model):
    creation_time = models.IntegerField()
    mod_time = models.IntegerField()
    deleted = models.IntegerField()
    time_start = models.IntegerField(primary_key=True)
    cpu_count = models.IntegerField()
    alloc_cpu_secs = models.BigIntegerField()
    down_cpu_secs = models.BigIntegerField()
    pdown_cpu_secs = models.BigIntegerField()
    idle_cpu_secs = models.BigIntegerField()
    resv_cpu_secs = models.BigIntegerField()
    over_cpu_secs = models.BigIntegerField()
    consumed_energy = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'prod_usage_hour_table'
        app_label = 'slurm'

class ProdUsageMonthTable(models.Model):
    creation_time = models.IntegerField()
    mod_time = models.IntegerField()
    deleted = models.IntegerField()
    time_start = models.IntegerField(primary_key=True)
    cpu_count = models.IntegerField()
    alloc_cpu_secs = models.BigIntegerField()
    down_cpu_secs = models.BigIntegerField()
    pdown_cpu_secs = models.BigIntegerField()
    idle_cpu_secs = models.BigIntegerField()
    resv_cpu_secs = models.BigIntegerField()
    over_cpu_secs = models.BigIntegerField()
    consumed_energy = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'prod_usage_month_table'
        app_label = 'slurm'

class ProdWckeyTable(models.Model):
    creation_time = models.IntegerField()
    mod_time = models.IntegerField()
    deleted = models.IntegerField()
    is_def = models.IntegerField()
    id_wckey = models.AutoField(primary_key=True)
    wckey_name = models.TextField()
    user = models.TextField()

    class Meta:
        managed = False
        db_table = 'prod_wckey_table'
        unique_together = (('wckey_name', 'user'),)
        app_label = 'slurm'

class ProdWckeyUsageDayTable(models.Model):
    creation_time = models.IntegerField()
    mod_time = models.IntegerField()
    deleted = models.IntegerField()
    id_wckey = models.IntegerField()
    time_start = models.IntegerField()
    alloc_cpu_secs = models.BigIntegerField(blank=True, null=True)
    resv_cpu_secs = models.BigIntegerField(blank=True, null=True)
    over_cpu_secs = models.BigIntegerField(blank=True, null=True)
    consumed_energy = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'prod_wckey_usage_day_table'
        unique_together = (('id_wckey', 'time_start'),)
        app_label = 'slurm'

class ProdWckeyUsageHourTable(models.Model):
    creation_time = models.IntegerField()
    mod_time = models.IntegerField()
    deleted = models.IntegerField()
    id_wckey = models.IntegerField()
    time_start = models.IntegerField()
    alloc_cpu_secs = models.BigIntegerField(blank=True, null=True)
    resv_cpu_secs = models.BigIntegerField(blank=True, null=True)
    over_cpu_secs = models.BigIntegerField(blank=True, null=True)
    consumed_energy = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'prod_wckey_usage_hour_table'
        unique_together = (('id_wckey', 'time_start'),)
        app_label = 'slurm'

class ProdWckeyUsageMonthTable(models.Model):
    creation_time = models.IntegerField()
    mod_time = models.IntegerField()
    deleted = models.IntegerField()
    id_wckey = models.IntegerField()
    time_start = models.IntegerField()
    alloc_cpu_secs = models.BigIntegerField(blank=True, null=True)
    resv_cpu_secs = models.BigIntegerField(blank=True, null=True)
    over_cpu_secs = models.BigIntegerField(blank=True, null=True)
    consumed_energy = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'prod_wckey_usage_month_table'
        unique_together = (('id_wckey', 'time_start'),)
        app_label = 'slurm'

class QosTable(models.Model):
    creation_time = models.IntegerField()
    mod_time = models.IntegerField()
    deleted = models.IntegerField(blank=True, null=True)
    name = models.TextField(unique=True)
    description = models.TextField(blank=True, null=True)
    flags = models.IntegerField(blank=True, null=True)
    grace_time = models.IntegerField(blank=True, null=True)
    max_jobs_per_user = models.IntegerField(blank=True, null=True)
    max_submit_jobs_per_user = models.IntegerField(blank=True, null=True)
    max_cpus_per_job = models.IntegerField(blank=True, null=True)
    max_cpus_per_user = models.IntegerField(blank=True, null=True)
    max_nodes_per_job = models.IntegerField(blank=True, null=True)
    max_nodes_per_user = models.IntegerField(blank=True, null=True)
    max_wall_duration_per_job = models.IntegerField(blank=True, null=True)
    max_cpu_mins_per_job = models.BigIntegerField(blank=True, null=True)
    max_cpu_run_mins_per_user = models.BigIntegerField(blank=True, null=True)
    grp_jobs = models.IntegerField(blank=True, null=True)
    grp_submit_jobs = models.IntegerField(blank=True, null=True)
    grp_cpus = models.IntegerField(blank=True, null=True)
    grp_mem = models.IntegerField(blank=True, null=True)
    grp_nodes = models.IntegerField(blank=True, null=True)
    grp_wall = models.IntegerField(blank=True, null=True)
    grp_cpu_mins = models.BigIntegerField(blank=True, null=True)
    grp_cpu_run_mins = models.BigIntegerField(blank=True, null=True)
    preempt = models.TextField()
    preempt_mode = models.IntegerField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    usage_factor = models.FloatField()
    usage_thres = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'qos_table'
        app_label = 'slurm'

class ResTable(models.Model):
    creation_time = models.IntegerField()
    mod_time = models.IntegerField()
    deleted = models.IntegerField(blank=True, null=True)
    name = models.TextField()
    description = models.TextField(blank=True, null=True)
    manager = models.TextField()
    server = models.TextField()
    count = models.IntegerField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    flags = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'res_table'
        unique_together = (('name', 'server', 'type'),)
        app_label = 'slurm'

class TableDefsTable(models.Model):
    creation_time = models.IntegerField()
    mod_time = models.IntegerField()
    table_name = models.TextField(primary_key=True)
    definition = models.TextField()

    class Meta:
        managed = False
        db_table = 'table_defs_table'
        app_label = 'slurm'

class TxnTable(models.Model):
    timestamp = models.IntegerField()
    action = models.SmallIntegerField()
    name = models.TextField()
    actor = models.TextField()
    cluster = models.TextField()
    info = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'txn_table'
        app_label = 'slurm'

class UohAssocTable(models.Model):
    creation_time = models.IntegerField()
    mod_time = models.IntegerField()
    deleted = models.IntegerField()
    is_def = models.IntegerField()
    id_assoc = models.AutoField(primary_key=True)
    user = models.TextField()
    acct = models.TextField()
    partition = models.TextField()
    parent_acct = models.TextField()
    lft = models.IntegerField()
    rgt = models.IntegerField()
    shares = models.IntegerField()
    max_jobs = models.IntegerField(blank=True, null=True)
    max_submit_jobs = models.IntegerField(blank=True, null=True)
    max_cpus_pj = models.IntegerField(blank=True, null=True)
    max_nodes_pj = models.IntegerField(blank=True, null=True)
    max_wall_pj = models.IntegerField(blank=True, null=True)
    max_cpu_mins_pj = models.BigIntegerField(blank=True, null=True)
    max_cpu_run_mins = models.BigIntegerField(blank=True, null=True)
    grp_jobs = models.IntegerField(blank=True, null=True)
    grp_submit_jobs = models.IntegerField(blank=True, null=True)
    grp_cpus = models.IntegerField(blank=True, null=True)
    grp_mem = models.IntegerField(blank=True, null=True)
    grp_nodes = models.IntegerField(blank=True, null=True)
    grp_wall = models.IntegerField(blank=True, null=True)
    grp_cpu_mins = models.BigIntegerField(blank=True, null=True)
    grp_cpu_run_mins = models.BigIntegerField(blank=True, null=True)
    def_qos_id = models.IntegerField(blank=True, null=True)
    qos = models.TextField()
    delta_qos = models.TextField()

    class Meta:
        managed = False
        db_table = 'uoh_assoc_table'
        unique_together = (('user', 'acct', 'partition'),)
        app_label = 'slurm'

class UohAssocUsageDayTable(models.Model):
    creation_time = models.IntegerField()
    mod_time = models.IntegerField()
    deleted = models.IntegerField()
    id_assoc = models.IntegerField()
    time_start = models.IntegerField()
    alloc_cpu_secs = models.BigIntegerField()
    consumed_energy = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'uoh_assoc_usage_day_table'
        unique_together = (('id_assoc', 'time_start'),)
        app_label = 'slurm'

class UohAssocUsageHourTable(models.Model):
    creation_time = models.IntegerField()
    mod_time = models.IntegerField()
    deleted = models.IntegerField()
    id_assoc = models.IntegerField()
    time_start = models.IntegerField()
    alloc_cpu_secs = models.BigIntegerField()
    consumed_energy = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'uoh_assoc_usage_hour_table'
        unique_together = (('id_assoc', 'time_start'),)
        app_label = 'slurm'

class UohAssocUsageMonthTable(models.Model):
    creation_time = models.IntegerField()
    mod_time = models.IntegerField()
    deleted = models.IntegerField()
    id_assoc = models.IntegerField()
    time_start = models.IntegerField()
    alloc_cpu_secs = models.BigIntegerField()
    consumed_energy = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'uoh_assoc_usage_month_table'
        unique_together = (('id_assoc', 'time_start'),)
        app_label = 'slurm'

class UohEventTable(models.Model):
    time_start = models.IntegerField()
    time_end = models.IntegerField()
    node_name = models.TextField()
    cluster_nodes = models.TextField()
    cpu_count = models.IntegerField()
    reason = models.TextField()
    reason_uid = models.IntegerField()
    state = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'uoh_event_table'
        unique_together = (('node_name', 'time_start'),)
        app_label = 'slurm'

class UohJobTable(models.Model):
    job_db_inx = models.AutoField(primary_key=True)
    mod_time = models.IntegerField()
    deleted = models.IntegerField()
    account = models.TextField(blank=True, null=True)
    cpus_req = models.IntegerField()
    cpus_alloc = models.IntegerField()
    derived_ec = models.IntegerField()
    derived_es = models.TextField(blank=True, null=True)
    exit_code = models.IntegerField()
    job_name = models.TextField()
    id_assoc = models.IntegerField()
    id_block = models.TextField(blank=True, null=True)
    id_job = models.IntegerField()
    id_qos = models.IntegerField()
    id_resv = models.IntegerField()
    id_wckey = models.IntegerField()
    id_user = models.IntegerField()
    id_group = models.IntegerField()
    kill_requid = models.IntegerField()
    mem_req = models.IntegerField()
    nodelist = models.TextField(blank=True, null=True)
    nodes_alloc = models.IntegerField()
    node_inx = models.TextField(blank=True, null=True)
    partition = models.TextField()
    priority = models.IntegerField()
    state = models.SmallIntegerField()
    timelimit = models.IntegerField()
    time_submit = models.IntegerField()
    time_eligible = models.IntegerField()
    time_start = models.IntegerField()
    time_end = models.IntegerField()
    time_suspended = models.IntegerField()
    gres_req = models.TextField()
    gres_alloc = models.TextField()
    gres_used = models.TextField()
    wckey = models.TextField()
    track_steps = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'uoh_job_table'
        unique_together = (('id_job', 'id_assoc', 'time_submit'),)
        app_label = 'slurm'

class UohLastRanTable(models.Model):
    hourly_rollup = models.IntegerField()
    daily_rollup = models.IntegerField()
    monthly_rollup = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'uoh_last_ran_table'
        app_label = 'slurm'

class UohResvTable(models.Model):
    id_resv = models.IntegerField()
    deleted = models.IntegerField()
    assoclist = models.TextField()
    cpus = models.IntegerField()
    flags = models.SmallIntegerField()
    nodelist = models.TextField()
    node_inx = models.TextField()
    resv_name = models.TextField()
    time_start = models.IntegerField()
    time_end = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'uoh_resv_table'
        unique_together = (('id_resv', 'time_start'),)
        app_label = 'slurm'

class UohStepTable(models.Model):
    job_db_inx = models.IntegerField()
    deleted = models.IntegerField()
    cpus_alloc = models.IntegerField()
    exit_code = models.IntegerField()
    id_step = models.IntegerField()
    kill_requid = models.IntegerField()
    nodelist = models.TextField()
    nodes_alloc = models.IntegerField()
    node_inx = models.TextField(blank=True, null=True)
    state = models.SmallIntegerField()
    step_name = models.TextField()
    task_cnt = models.IntegerField()
    task_dist = models.SmallIntegerField()
    time_start = models.IntegerField()
    time_end = models.IntegerField()
    time_suspended = models.IntegerField()
    user_sec = models.IntegerField()
    user_usec = models.IntegerField()
    sys_sec = models.IntegerField()
    sys_usec = models.IntegerField()
    max_pages = models.IntegerField()
    max_pages_task = models.IntegerField()
    max_pages_node = models.IntegerField()
    ave_pages = models.FloatField()
    max_rss = models.BigIntegerField()
    max_rss_task = models.IntegerField()
    max_rss_node = models.IntegerField()
    ave_rss = models.FloatField()
    max_vsize = models.BigIntegerField()
    max_vsize_task = models.IntegerField()
    max_vsize_node = models.IntegerField()
    ave_vsize = models.FloatField()
    min_cpu = models.IntegerField()
    min_cpu_task = models.IntegerField()
    min_cpu_node = models.IntegerField()
    ave_cpu = models.FloatField()
    act_cpufreq = models.FloatField()
    consumed_energy = models.FloatField()
    req_cpufreq = models.IntegerField()
    max_disk_read = models.FloatField()
    max_disk_read_task = models.IntegerField()
    max_disk_read_node = models.IntegerField()
    ave_disk_read = models.FloatField()
    max_disk_write = models.FloatField()
    max_disk_write_task = models.IntegerField()
    max_disk_write_node = models.IntegerField()
    ave_disk_write = models.FloatField()

    class Meta:
        managed = False
        db_table = 'uoh_step_table'
        unique_together = (('job_db_inx', 'id_step'),)
        app_label = 'slurm'

class UohSuspendTable(models.Model):
    job_db_inx = models.IntegerField()
    id_assoc = models.IntegerField()
    time_start = models.IntegerField()
    time_end = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'uoh_suspend_table'
        app_label = 'slurm'

class UohUsageDayTable(models.Model):
    creation_time = models.IntegerField()
    mod_time = models.IntegerField()
    deleted = models.IntegerField()
    time_start = models.IntegerField(primary_key=True)
    cpu_count = models.IntegerField()
    alloc_cpu_secs = models.BigIntegerField()
    down_cpu_secs = models.BigIntegerField()
    pdown_cpu_secs = models.BigIntegerField()
    idle_cpu_secs = models.BigIntegerField()
    resv_cpu_secs = models.BigIntegerField()
    over_cpu_secs = models.BigIntegerField()
    consumed_energy = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'uoh_usage_day_table'
        app_label = 'slurm'

class UohUsageHourTable(models.Model):
    creation_time = models.IntegerField()
    mod_time = models.IntegerField()
    deleted = models.IntegerField()
    time_start = models.IntegerField(primary_key=True)
    cpu_count = models.IntegerField()
    alloc_cpu_secs = models.BigIntegerField()
    down_cpu_secs = models.BigIntegerField()
    pdown_cpu_secs = models.BigIntegerField()
    idle_cpu_secs = models.BigIntegerField()
    resv_cpu_secs = models.BigIntegerField()
    over_cpu_secs = models.BigIntegerField()
    consumed_energy = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'uoh_usage_hour_table'
        app_label = 'slurm'

class UohUsageMonthTable(models.Model):
    creation_time = models.IntegerField()
    mod_time = models.IntegerField()
    deleted = models.IntegerField()
    time_start = models.IntegerField(primary_key=True)
    cpu_count = models.IntegerField()
    alloc_cpu_secs = models.BigIntegerField()
    down_cpu_secs = models.BigIntegerField()
    pdown_cpu_secs = models.BigIntegerField()
    idle_cpu_secs = models.BigIntegerField()
    resv_cpu_secs = models.BigIntegerField()
    over_cpu_secs = models.BigIntegerField()
    consumed_energy = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'uoh_usage_month_table'
        app_label = 'slurm'

class UohWckeyTable(models.Model):
    creation_time = models.IntegerField()
    mod_time = models.IntegerField()
    deleted = models.IntegerField()
    is_def = models.IntegerField()
    id_wckey = models.AutoField(primary_key=True)
    wckey_name = models.TextField()
    user = models.TextField()

    class Meta:
        managed = False
        db_table = 'uoh_wckey_table'
        unique_together = (('wckey_name', 'user'),)
        app_label = 'slurm'

class UohWckeyUsageDayTable(models.Model):
    creation_time = models.IntegerField()
    mod_time = models.IntegerField()
    deleted = models.IntegerField()
    id_wckey = models.IntegerField()
    time_start = models.IntegerField()
    alloc_cpu_secs = models.BigIntegerField(blank=True, null=True)
    resv_cpu_secs = models.BigIntegerField(blank=True, null=True)
    over_cpu_secs = models.BigIntegerField(blank=True, null=True)
    consumed_energy = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'uoh_wckey_usage_day_table'
        unique_together = (('id_wckey', 'time_start'),)
        app_label = 'slurm'

class UohWckeyUsageHourTable(models.Model):
    creation_time = models.IntegerField()
    mod_time = models.IntegerField()
    deleted = models.IntegerField()
    id_wckey = models.IntegerField()
    time_start = models.IntegerField()
    alloc_cpu_secs = models.BigIntegerField(blank=True, null=True)
    resv_cpu_secs = models.BigIntegerField(blank=True, null=True)
    over_cpu_secs = models.BigIntegerField(blank=True, null=True)
    consumed_energy = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'uoh_wckey_usage_hour_table'
        unique_together = (('id_wckey', 'time_start'),)
        app_label = 'slurm'

class UohWckeyUsageMonthTable(models.Model):
    creation_time = models.IntegerField()
    mod_time = models.IntegerField()
    deleted = models.IntegerField()
    id_wckey = models.IntegerField()
    time_start = models.IntegerField()
    alloc_cpu_secs = models.BigIntegerField(blank=True, null=True)
    resv_cpu_secs = models.BigIntegerField(blank=True, null=True)
    over_cpu_secs = models.BigIntegerField(blank=True, null=True)
    consumed_energy = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'uoh_wckey_usage_month_table'
        unique_together = (('id_wckey', 'time_start'),)
        app_label = 'slurm'

class UserTable(models.Model):
    creation_time = models.IntegerField()
    mod_time = models.IntegerField()
    deleted = models.IntegerField(blank=True, null=True)
    name = models.TextField(primary_key=True)
    admin_level = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'user_table'
        app_label = 'slurm'
