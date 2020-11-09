# flask-users-microservice-with-jwt-extended

## Requirements

Config virtualenv:

```bash
$ git clone https://github.com/eadomenech/flask-users-microservice-with-jwt-extended.git src
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r src/requirements.txt
```

## For development

1- Install pytest, coverage and flake8

```bash
$ pip install pytest==5.0.1 pytest-cov flake8
```

2- Create `users-dev` and `users-test` local postgres databases.

3- Create a .env file in the src folder and add the following:

```bash
FLASK_APP=application:create_app('config.DevelopmentConfig')
DATABASE_DEV_URL=postgresql://user:password@localhost:5432/users-dev
DATABASE_TEST_URL=postgresql://user:password@localhost:5432/users-test
```

4- Generate a `jwt-key.pub` and `jwt-key` public/private key set. The name of the file where the key will be stored must be `jwt-key`.

```bash
(venv) $ ssh-keygen -t rsa -b 4096
Generating public/private rsa key pair.
Enter file in which to save the key (/home/ernesto/.ssh/id_rsa): jwt-key
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in jwt-key.
Your public key has been saved in jwt-key.pub.
The key fingerprint is:
SHA256:bpE00rWJmcdms0e2jw4YBzqEmZd19NgvpVUX3M3EQzg ernesto@Dell
The key's randomart image is:
+---[RSA 4096]----+
|        ..+   +*B|
|     + + B * E +*|
|    + = O X = + .|
|     o + B = *   |
|      o S o = .  |
|       o = . +   |
|        + . . .  |
|       .   o     |
|            .    |
+----[SHA256]-----+
```

5- Create a `private` folder inside the `src` folder and copy the keys inside it.

6- Database init:

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
