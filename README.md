# flask-microservice-users-with-jwt-extended

## Requirements

Config virtualenv:

```bash
git clone https://github.com/eadomenech/flask-microservice-users-with-jwt-extended.git src
python3 -m venv env
source env/bin/activate
pip install -r src/requirements.txt
```

## For development

```bash
pip install pytest==5.0.1 pytest-cov flake8
```

Create local postgres database.
Create a .env file in the src folder and add the following:

```bash
FLASK_APP=application:create_app('config.DevelopmentConfig')
DATABASE_DEV_URL=postgresql://user:password@localhost:5432/database-dev
DATABASE_TEST_URL=postgresql://user:password@localhost:5432/database-test
```

Database init:

```bash
$ cd src/
$ flask db init
$ flask db migrate
$ flask db upgrade
```

Run tests:

```bash
pytest --cov-report term-missing --cov
```

Code quality:

```bash
flake8 application tests
```

## Run the app

```bash
python app.py
```
