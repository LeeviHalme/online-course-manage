from flask import Blueprint, render_template
from sampleData import sampleCourses

main = Blueprint("main", __name__)

# a simple page that says hello
@main.route("/")
def index():
    return render_template("home.html", courses=sampleCourses)
