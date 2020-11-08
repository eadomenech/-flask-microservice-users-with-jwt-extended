from datetime import datetime
import uuid

from flask import current_app
from sqlalchemy.dialects.postgresql import UUID

from application import db, bcrypt


class User(db.Model):
    id = db.Column(
        UUID(as_uuid=True), primary_key=True,
        default=uuid.uuid4, unique=True, nullable=False)
    username = db.Column(
        db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    created = db.Column(db.DateTime(), default=datetime.now(), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password.encode(
                'utf-8'), current_app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()

    def __repr__(self):
        return '<User {}>'.format(self.id)

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'active': self.active,
            'created': self.created
        }
