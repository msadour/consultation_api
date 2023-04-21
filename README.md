# Coding test Medbelle


## Installation

### Setup dev environment

1. Install a virtual environment : ```virtualenv .venv```
2. Activate environment : ```.\.venv\Scripts\activate``` (or ```source ./.venv/bin/activate``` under Linux)
3. Install dependencies : ```pip install -r requirements.txt```
4. Install pre-commit : ```pre-commit install```

### Setup database

1. Put the ```.env``` file, which is on the email, in the folder consultation_api (inside the project)
2. Check this file regarding your database setup (db user, db port ...)
3. Create a database named consultation_api
4. Create tables and users :
   1. Migrate : ```python manage.py migrate```
   2. Create users : ```python manage.py initdata```


## Utilisation

- Launch the server ```python manage.py runserver```
- You can see the usage of the API for patients and surgeons in documentations folder
- Admin panel : http://127.0.0.1:8000/admin