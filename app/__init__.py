# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager, current_user
from flask_bootstrap import Bootstrap


db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name='SQLALCHEMY_DATABASE_URI'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # db = SQLAlchemy(app)
    db.init_app(app)

    with app.test_request_context():
        db.create_all()

    bootstrap.init_app(app)
    login_manager.init_app(app)

    #  BluePrint ------- start
    from auth import auth as auth_blueprint
    from main import main as main_blueprint
    from game import game as game_blueprint
    from zabbix import zabbix as zabbix_blueprint
    from dataapi import dataapi as dataapi_blueprint
    from dataviews import dataviews as dataviews_blueprint
    from salt import salt as salt_blueprint

    app.register_blueprint(salt_blueprint)
    app.register_blueprint(dataapi_blueprint,url_prefix='/dataapi')
    app.register_blueprint(dataviews_blueprint,url_prefix='/dataviews')
    app.register_blueprint(zabbix_blueprint)
    app.register_blueprint(game_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    #  BluePrint ------- end



    return app
