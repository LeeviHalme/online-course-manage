import os
from flask import Flask, render_template
from dotenv import load_dotenv


def create_app(test_config=None):
    # load .env file
    load_dotenv()

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route("/")
    def index():
        return render_template("home.html", debug=os.getenv("FLASK_DEBUG"))

    # app login page
    @app.route("/login")
    def login():
        return render_template("login.html")

    # app register page
    @app.route("/register")
    def register():
        return render_template("register.html")

    return app
