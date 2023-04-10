from flask import Blueprint, render_template
from sampleData import sampleCourses

main = Blueprint("main", __name__)


# app homepage route
@main.route("/")
def index():
    return render_template("home.html", courses=sampleCourses)
