from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap


db = SQLAlchemy()

def create_app():

    app = Flask(__name__)

    Bootstrap(app)
    db.init_app(app)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    return app
