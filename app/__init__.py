#!/usr/bin/env python
# coding: utf-8

# import library

from flask import Flask
from flask_login.utils import login_user
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager 



#app.config.from_object(config)

db = SQLAlchemy()

def create_app():
    # Init flask app 
    app = Flask(__name__)

    app.config['SECRET_KEY'] =  'this'
    #app.config.update(SECRET_KEY=os.urandom(24))
    app.config['SQLALCHEMY_DATABASE_URI']  = 'mysql+pymysql://hachem:tigertiger@localhost/ACCIDENT_USERS'
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .views import app as main_blueprint
    app.register_blueprint(main_blueprint)
    return app

# import library
# from app import views
# from app import models


