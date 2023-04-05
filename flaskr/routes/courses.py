from sampleData import sampleCourses
from flask import Blueprint, render_template, abort

courses = Blueprint("courses", __name__, url_prefix="/courses")

# view all public courses page
@courses.route("/")
def show_courses():
    return render_template(
        "courses.html", courses=sampleCourses, searchTerm="example search term"
    )


# view course info page
@courses.route("/<course_id>")
def view_course(course_id):
    ids = list(map(lambda c: c[3], sampleCourses))

    # if id not found
    if course_id not in ids:
        return abort(404)

    course = sampleCourses[ids.index(course_id)]

    return render_template("view_course.html", course=course)
