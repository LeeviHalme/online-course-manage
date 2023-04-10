import os
from flask import Flask
from dotenv import load_dotenv

# import blueprints
from routes.main import main
from routes.auth import auth
from routes.courses import courses
from routes.profile import profile


def create_app():
    # load .env file
    load_dotenv()

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # init database here in order to
    # access correct app context
    from modules.db import db

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("POSTGRES_URI")
    db.init_app(app)

    # setup session keys
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    # register blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(courses)
    app.register_blueprint(profile)

    return app
