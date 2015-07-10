class SlurmRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'slurm':
            return 'slurm'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'slurm':
            return 'slurm'
        return None

    def allow_relation(self, obj1, obj2, **hints):

        if obj1._meta.app_label == 'slurm' and obj2._meta == 'slurm':
            return True
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        if app_label == 'slurm':
            return db == 'slurm'
        return None
        
