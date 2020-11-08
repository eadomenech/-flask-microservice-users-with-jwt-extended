import datetime

from sqlalchemy.exc import IntegrityError
import pytest
from uuid import UUID

from tests.utils import TestBaseModel
from application import db
from application.api.models import User


class TestCampaignModel(TestBaseModel):

    def test_add_user(self, app):
        user = self.add_user()
        assert user.username == 'user1'
        assert user.email == 'user1@example.com'
        assert user.active == True
        assert user.password

    def test_add_user_duplicate_username(self, app):
        user = self.add_user()
        duplicate_user = User(
            username='user1', email='user1@example.com',
            password='p@ssw0rd')
        db.session.add(duplicate_user)
        with pytest.raises(IntegrityError):
            db.session.commit()

    def test_to_json(self, app):
        user = self.add_user()
        assert isinstance(user.to_json(), dict)

    def test_passwords_are_random(self, app):
        user_one = self.add_user(
            username='user1', email='user1@example.com',
            password='password')
        user_two = self.add_user(
            username='user2', email='user2@example.com',
            password='password')
        assert user_one.password != user_two.password
