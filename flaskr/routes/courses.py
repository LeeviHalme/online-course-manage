from flask import Blueprint, render_template, abort, request
from modules.courses import get_courses, search_courses_by_name, find_by_id

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
@courses.route("/<course_id>")
def view_course(course_id: str):
    course = find_by_id(course_id)

    # if course was not found
    if not course:
        return abort(404)

    return render_template("view_course.html", course=course)
