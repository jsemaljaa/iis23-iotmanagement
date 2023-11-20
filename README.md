# TODOs
- fix heroku build
- implement models
- find out users groups & roles
- make basic html pages of the system
- create views 
- test database connection



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