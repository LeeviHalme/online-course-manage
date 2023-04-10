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
    user = session["user"]

    # if user is not logged in
    if not user:
        return abort(401)

    # show correct dashboard
    # depending on user type
    if user["type"] == "STUDENT":
        # get courses user participates
        courses = get_enrolled_courses(user["id"])

        return render_template("student_dashboard.html", courses=courses)
    elif user["type"] == "TEACHER":
        return render_template("teacher_dashboard.html")
