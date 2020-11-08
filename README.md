# flask-microservice-users-with-jwt-extended

Config virtualenv:

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
pip install pytest==5.0.1 pytest-cov flake8
```

Run tests:

```bash
pytest --cov-report term-missing --cov
```

Code quality:

```bash
flake8 application tests
```

Run the app:

```bash
python app.py
```
