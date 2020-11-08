from application import db
from application.api.models import User


class TestBaseModel(object):
    def add_user(
            self, username='user1', email='user1@example.com',
            password='p@ssw0rd', active=True):
        user = User(username, email, password)
        db.session.add(user)
        db.session.commit()
        return user
