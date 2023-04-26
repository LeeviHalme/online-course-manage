from flask import Blueprint, render_template, abort, redirect, session, request, flash
from modules.profile import get_enrolled_courses, validate_email_list
from modules.courses import create_course
from datetime import datetime
import utils.validators as validate

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
def create_course_route():
    # if user is not logged in
    user = session.get("user")
    if not user:
        return abort(401)

    # if user is not a teacher
    if user["type"] != "TEACHER":
        return abort(403)

    # if this was GET request, return the form
    if request.method == "GET":
        return render_template("teacher/create_course.html")

    # get request body
    values = request.form
    name = values.get("name")
    short_description = values.get("short_description")
    description = values.get("description")
    invitation_code = values.get("invitation_code")
    course_teachers = values.get("course_teachers[]")
    is_hidden = values.get("is_hidden")
    is_public = values.get("is_public")

    # validate name (5-120 chars)
    if len(name) < 5 or len(name) > 120:
        flash("Invalid name! Must be between 5-120 chars", "danger")
        return redirect(request.url)

    # validate short description (0-120 chars)
    elif len(short_description) > 120:
        flash("Invalid short description! Max 120 chars")
        return redirect(request.url)

    # validate description (string)
    elif type(description) != str:
        flash("Invalid description!")
        return redirect(request.url)

    # validate invitation code (alphanumeric, max 15 chars)
    elif not validate.alpha(invitation_code) or len(invitation_code) > 15:
        flash("Invalid invitation code! Max 15 characters (a-Z, 0-9)", "danger")
        return redirect(request.url)

    # validate is_hidden checkbox
    elif is_hidden and not validate.boolean(is_hidden):
        flash("Invalid is_hidden flag value", "danger")
        return redirect(request.url)

    # validate is_public checkbox
    elif is_public and not validate.boolean(is_public):
        flash("Invalid is_public flag value", "danger")
        return redirect(request.url)

    # validate teachers email array
    teacher_list = course_teachers.split(",")
    valid = validate_email_list("TEACHER", teacher_list)

    # if email list was not valid
    if not valid:
        flash(
            "Invalid teachers! Make sure you entered registered teachers email's only.",
            "danger",
        )
        return redirect(request.url)

    # create new course
    create_course(
        name, short_description, description, invitation_code, is_hidden, is_public
    )

    # show success msg
    flash("Successfully created new course!", "success")

    return redirect("/profile/dashboard")
