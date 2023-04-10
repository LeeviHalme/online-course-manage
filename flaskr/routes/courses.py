from flask import Blueprint, render_template, abort, request, redirect, session
from modules.courses import (
    get_courses,
    search_courses_by_name,
    find_by_id,
    is_enrolled,
    validate_invitation_code,
    enroll_to_course,
)
from modules.db import serialize_to_dict

courses = Blueprint("courses", __name__, url_prefix="/courses")


# view all public courses page
@courses.route("/", methods=["GET"])
def show_courses():
    query = request.args.to_dict()
    searchTerm = query.get("search")

    # if user performed a search
    if searchTerm:
        # get courses by name from db
        courses = search_courses_by_name(searchTerm)

        return render_template("courses.html", courses=courses, searchTerm=searchTerm)
    else:
        # get public courses from db
        courses = get_courses()

        return render_template("courses.html", courses=courses)


# view course info page
@courses.route("/<course_id>", methods=["GET"])
def view_course(course_id: str):
    course = find_by_id(course_id)

    # if course was not found
    if not course:
        return abort(404)

    # check additional state passed
    args = request.args.to_dict()
    alert = None
    if args.get("alreadyEnrolled"):
        alert = ("danger", "You've already enrolled to this course!")
    elif args.get("invalidCode"):
        alert = ("danger", "Invalid invitation code! Please double-check spelling")

    return render_template(
        "view_course.html", course=serialize_to_dict(course), alert=alert
    )


# enroll to a course
@courses.route("/<course_id>/join", methods=["POST"])
def enroll(course_id: str):
    # if user is not logged in
    user = session["user"]
    if not user:
        return abort(401)

    # get request body
    code = request.form["invitation_code"]

    # TODO: Validate request body

    # get course from db
    course = find_by_id(course_id)

    # if course doesn't exist
    if not course:
        return abort(404)

    enrolled = is_enrolled(course_id, user["id"])

    # if user is already enrolled
    if enrolled:
        return redirect(f"/courses/{course_id}?alreadyEnrolled=true")

    valid = validate_invitation_code(course_id, code)

    # if invite code was not valid
    if not valid:
        return redirect(f"/courses/{course_id}?invalidCode=true")

    # create new participant record
    enroll_to_course(course_id, user["id"])

    return redirect(f"/courses/{course_id}")
