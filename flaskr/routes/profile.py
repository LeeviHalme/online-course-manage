from flask import Blueprint, render_template, abort, session
from modules.profile import get_enrolled_courses
from datetime import datetime

profile = Blueprint("profile", __name__, url_prefix="/profile")


# router utils
@profile.context_processor
def context_processor():
    # format date
    def format_date(date: datetime):
        return date.strftime("%d/%m/%Y")

    return dict(format_date=format_date)


# dashboard route
@profile.route("/dashboard", methods=["GET"])
def dashboard():
    # if user is not logged in
    user = session.get("user")
    if not user:
        return abort(401)

    # get courses user participates
    courses = get_enrolled_courses(user["id"])

    return render_template("dashboard.html", courses=courses)


# create course route
@profile.route("/dashboard/create-course", methods=["GET", "POST"])
def create_course():
    # if user is not logged in
    user = session.get("user")
    if not user:
        return abort(401)

    # if user is not a teacher
    if user["type"] != "TEACHER":
        return abort(403)

    return render_template("teacher/create_course.html")
