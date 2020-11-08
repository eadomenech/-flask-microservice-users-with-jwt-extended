# flask-microservice-users-with-jwt-extended

Config virtualenv:

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
pip install pytest==5.0.1 pytest-cov
```

Run tests:

```bash
pytest --cov-report term-missing --cov
```

Run the app:

```bash
python app.py
```
