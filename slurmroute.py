class SlurmRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'slurm_manager':
            return 'slurm'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'slurm_manager':
            return 'slurm'
        return None

    def allow_relation(self, obj1, obj2, **hints):

        if obj1._meta.app_label == 'slurm_manager' and obj2._meta.app_label == 'slurm_manager':
            return True
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        if app_label == 'slurm_manager':
            return db == 'slurm'
        return None

    def allow_syncdb(self, db, model):
        if db == 'slurm':
            return model._meta.app_label == 'slurm_manager'
        elif model._meta.app_label == 'slurm_manager':
            return False
        return None
                        
