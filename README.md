# TODO's Alina
* test stuff
* create sql script to fill the database with reference data


# Documentation

## Prerequesites

### Heroku
Install Heroku Command Line Interface: https://devcenter.heroku.com/articles/heroku-cli  
  
Usage: when in root folder
```Bash
heroku login
heroku git:remote -a iot-management
```
Useful Heroku commands
```Bash
# app's configuration key-values
heroku config -s
#
heroku pg:push postgres://localhost/iotmanagement postgresql-horizontal-68677
```

Push local postgresql DB to Heroku (Alina's PowerShell):
```Bash
$env:PGUSER="jsemalja"; $env:PGPASSWORD="jsemalja"; heroku pg:push iotmanagement DATABASE_URL -a iotmanagement
```

### Virtual Environment

To launch virtual environment:
```Bash
env\Scripts\activate
```

Generate secret key for .env:
```Bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### PostgreSQL
To reach postgresql in CLI
```Bash
psql -U your_username -h localhost -d postgres
# List of all databases
\l
# To connect to local database
\c db_name
```

### Django
To execute script in Django shell
```Bash
python ./manage.py shell < myscript.py
```
To run the server for whole local network
```Bash
python manage.py runserver 0.0.0.0:8000
```