"""Welcome to Users API.

# Overview

Here we have an overview of Users API
"""
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from apifairy import APIFairy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
import logging
from logging.handlers import SMTPHandler
from flask_jwt_extended import JWTManager


# Instantiate
db = SQLAlchemy()
ma = Marshmallow()
apifairy = APIFairy()
migrate = Migrate()
bcrypt = Bcrypt()
jwtManager = JWTManager()


def create_app(config):
    """Application setup"""
    app = Flask(__name__, instance_relative_config=False)

    # load the config
    app.config.from_object(config)

    # enable CORS
    CORS(app)

    # set up extensions
    db.init_app(app)
    ma.init_app(app)
    apifairy.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwtManager.init_app(app)

    with app.app_context():
        # load some plugins, modules or blueprints
        from application.api.v1.users import api as users
        from application.api.v1.auth import api as auth

        # registrar los blueprints
        app.register_blueprint(users, url_prefix='/api/v1')
        app.register_blueprint(auth, url_prefix='/api/v1/auth')

        if not app.debug:
            if app.config['MAIL_SERVER']:
                auth = None
                if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                    auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
                secure = None
                if app.config['MAIL_USE_TLS']:
                    secure = ()
                mail_handler = SMTPHandler(
                    mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                    fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                    toaddrs=app.config['ADMINS'], subject='Quimero Backend Failure',
                    credentials=auth, secure=secure)
                mail_handler.setLevel(logging.ERROR)
                app.logger.addHandler(mail_handler)

        @app.route('/swagger')
        def swagger():
            return render_template(
                'apifairy/swagger_ui.html', title=apifairy.title,
                version=apifairy.version)

    return app
