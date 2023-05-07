from flask import Blueprint, render_template, abort, redirect, session, request, flash
from modules.profile import get_enrolled_courses, validate_email_list
from modules.courses import (
    create_course,
    update_course,
    create_material,
    find_by_id,
    is_enrolled,
    get_course_invitation_code,
)
from modules.submissions import get_user_submissions
from datetime import datetime
import utils.validators as validate

profile = Blueprint("profile", __name__, url_prefix="/profile")


# router utils
@profile.context_processor
def context_processor():
    # format date
    def format_date(date: datetime):
        return date.strftime("%d/%m/%Y %H:%M")

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

    # get user submissions
    submissions = get_user_submissions(user["id"])

    return render_template("dashboard.html", courses=courses, submissions=submissions)


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
    course_teachers = values.getlist("course_teachers[]")
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
    elif not invitation_code.isalnum() or len(invitation_code) > 15:
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
    valid = validate_email_list("TEACHER", course_teachers)

    # if email list was not valid
    if not valid:
        flash(
            "Invalid teachers! Make sure you entered registered teachers email's only.",
            "danger",
        )
        return redirect(request.url)

    # create new course
    create_course(
        name,
        short_description,
        description,
        invitation_code,
        is_hidden,
        is_public,
        course_teachers,
    )

    # show success msg
    flash("Successfully created new course!", "success")

    return redirect("/profile/dashboard")


# edit course route
@profile.route("/dashboard/edit-course", methods=["POST"])
def edit_course():
    # if user is not logged in
    user = session.get("user")
    if not user:
        return abort(401)

    # if user is not a teacher
    if user["type"] != "TEACHER":
        return abort(403)

    # get request body
    values = request.form
    course_id = values.get("course_id")

    name = values.get("name")
    short_description = values.get("short_description")
    description = values.get("description")
    is_hidden = values.get("is_hidden")
    is_public = values.get("is_public")

    course = find_by_id(course_id)

    # if course was not found
    if not course:
        return abort(404)

    # if teacher isn't responsible for this course
    enrolled = is_enrolled(course_id, user["id"])
    if not enrolled:
        return abort(403)

    # validate name (5-120 chars)
    if len(name) < 5 or len(name) > 120:
        flash("Invalid name! Must be between 5-120 chars", "danger")
        return redirect(f"/courses/{course_id}/edit")

    # validate short description (0-120 chars)
    elif len(short_description) > 120:
        flash("Invalid short description! Max 120 chars")
        return redirect(f"/courses/{course_id}/edit")

    # validate description (string)
    elif type(description) != str:
        flash("Invalid description!")
        return redirect(f"/courses/{course_id}/edit")

    # validate is_hidden checkbox
    elif is_hidden and not validate.boolean(is_hidden):
        flash("Invalid is_hidden flag value", "danger")
        return redirect(f"/courses/{course_id}/edit")

    # validate is_public checkbox
    elif is_public and not validate.boolean(is_public):
        flash("Invalid is_public flag value", "danger")
        return redirect(f"/courses/{course_id}/edit")

    # update course information
    # invitation code is updated separately
    code = get_course_invitation_code(course_id)
    update_course(
        course_id,
        name,
        short_description,
        description,
        code,
        is_hidden,
        is_public,
    )

    # show success msg
    flash("Successfully updated the course!", "success")

    return redirect(f"/courses/{course_id}/edit")


# update invitation code
@profile.route("/dashboard/edit-invite", methods=["POST"])
def edit_invitation_code():
    # if user is not logged in
    user = session.get("user")
    if not user:
        return abort(401)

    # if user is not a teacher
    if user["type"] != "TEACHER":
        return abort(403)

    # get request body
    values = request.form
    course_id = values.get("course_id")
    invitation_code = values.get("invitation_code")

    course = find_by_id(course_id)

    # if course was not found
    if not course:
        return abort(404)

    # if teacher isn't responsible for this course
    enrolled = is_enrolled(course_id, user["id"])
    if not enrolled:
        return abort(403)

    # validate invitation code (alphanumeric, max 15 chars)
    if not invitation_code.isalnum() or len(invitation_code) > 15:
        flash("Invalid invitation code! Max 15 characters (a-Z, 0-9)", "danger")
        return redirect(f"/courses/{course_id}/edit")

    # update course information
    update_course(
        course_id,
        course.name,
        course.short_description,
        course.description,
        invitation_code,
        course.is_hidden,
        course.is_public,
    )

    # show success msg
    flash(
        "Successfully updated invite code! NOTE: See the question mark",
        "success",
    )

    return redirect(f"/courses/{course_id}/edit")


# create new material
@profile.route("/dashboard/create-material", methods=["POST"])
def create_material_route():
    # if user is not logged in
    user = session.get("user")
    if not user:
        return abort(401)

    # if user is not a teacher
    if user["type"] != "TEACHER":
        return abort(403)

    # get request body
    values = request.form
    course_id = values.get("course_id")
    name = values.get("name")
    content = values.get("content")

    course = find_by_id(course_id)

    # if course was not found
    if not course:
        return abort(404)

    # if teacher isn't responsible for this course
    enrolled = is_enrolled(course_id, user["id"])
    if not enrolled:
        return abort(403)

    # validate name (>0<25 chars)
    if not name or len(name) == 0 or len(name) > 25:
        flash(f"Invalid name! (Between 1 and 25 chars)", "danger")
        return redirect(f"/courses/{course_id}/edit")

    # validate content (>0 chars)
    elif not content or len(content) == 0:
        flash("Invalid content!", "danger")
        return redirect(f"/courses/{course_id}/edit")

    # create material on db
    create_material(course_id, name, content)

    # show success msg
    flash(
        "Successfully created material!",
        "success",
    )

    return redirect(f"/courses/{course_id}/edit")
