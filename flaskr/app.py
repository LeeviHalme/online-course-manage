import os
from flask import Flask, render_template, abort
from dotenv import load_dotenv
from sampleData import sampleCourses


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
        return render_template("home.html", courses=sampleCourses)

    # app login page
    @app.route("/login")
    def login():
        return render_template("login.html")

    # app register page
    @app.route("/register")
    def register():
        return render_template("register.html")

    # view all public courses page
    @app.route("/courses")
    def courses():
        return render_template(
            "courses.html", courses=sampleCourses, searchTerm="example search term"
        )

    # view course info page
    @app.route("/courses/<course_id>")
    def view_course(course_id):
        ids = list(map(lambda c: c[3], sampleCourses))

        # if id not found
        if course_id not in ids:
            return abort(404)

        course = sampleCourses[ids.index(course_id)]

        return render_template("view_course.html", course=course)

    return app
