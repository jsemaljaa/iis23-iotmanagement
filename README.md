# Documentation

## Prerequesites
Some prerequesites to launch a local server with the app

### Virtual Environment

To launch virtual environment:
```Bash
env\Scripts\activate
```

<details>
  <summary>In iotmanagement/iotmanagement folder create an .env file</summary>

  ```
  SECRET_KEY=django-insecure-(wn%etwu$e6eruy1-%z(zn!&=rrz_ozacc-_b64j8v(1qenrfm
  DB_NAME=
  DB_USER=
  DB_PASSWORD=
  DB_HOST=localhost
  DB_PORT=5432

  # Fill all the necessary data to be able to connect to your local PostgreSQL database
  ```
</details>

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
