Things that need to be configured outside the scope of this application

0. Download the django-cas project into the HPC_Portal directory (hg clone https://bitbucket.org/cpcc/django-cas ).  Move the django_cas directory out of the repo directory and place it inside the HPC_Portal directory (HPC_Portal/django_cas) 

1. uncomment in the top-level urls.py the admin line, and add two lines:
```
    url(r'^accounts/login/$', 'django_cas.views.login'), 
    url(r'^accounts/logout/$', 'django_cas.views.logout'),
```

2. Move the slurm database off the default and create a new default database (create database , grant all on db user, and syncdb).  
Make sure to use your username when asked about the super user, or we will be locked out of the admin pages with CAS enabled. 
```
DATABASES = {
    'default': {
	'NAME': 'portal',
    },

    'slurm': {
        'NAME': 'slurm',
    }
}
```


3. Add to the settings.py 
```
DATABASE_ROUTERS=['slurm_manager.slurmroute.SlurmRouter']
```
Allows us to route all slurm models to the correct database

4. set the STATIC_ROOT to the following:
```
STATIC_ROOT = os.path.join(BASE_DIR, "HPC_Portal", "static")
```

5. run manager.py collectstatic

6. change the conf/httpd-app.conf to contain an alias for /static/
Alias /static/ "<path_to_project>/HPC_Portal/HPC_Portal/static/"

7. add to settings.py the following CAS parameters:
```
CAS_SERVER_URL='<cas_server_url>/cas/'
CAS_LOGOUT_COMPLETELY = True
CAS_VERSION = '2'
```
