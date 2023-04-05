import os
from flask import Flask
from dotenv import load_dotenv

# import blueprints
from routes.main import main
from routes.auth import auth
from routes.courses import courses


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

    # register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(courses)
    app.register_blueprint(main)

    return app
