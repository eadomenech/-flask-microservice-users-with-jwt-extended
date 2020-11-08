import pytest

from application import create_app
from application import db


@pytest.fixture
def app():
    app = create_app('config.TestingConfig')

    with app.app_context():
        db.create_all()
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()



@pytest.fixture
def client(app):

    with app.test_client() as client:
        yield client
