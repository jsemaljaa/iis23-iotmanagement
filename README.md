
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



To launch virtual environment:
```Bash
env\Scripts\activate
```

Generate secret key for .env:
```Bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

