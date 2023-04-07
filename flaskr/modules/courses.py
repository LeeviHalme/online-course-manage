from modules.db import make_query

# get all courses from db
def get_courses(hidden=False):
    # if visible courses were requested
    if not hidden:
        query = make_query("SELECT * FROM courses WHERE NOT is_hidden")
        courses = query.fetchall()
        return courses
    else:
        query = make_query("SELECT * FROM courses")
        courses = query.fetchall()
        return courses


# search courses by their name
def search_courses_by_name(name: str):
    query = make_query(
        "SELECT * FROM courses WHERE UPPER(name) LIKE UPPER(:name)",
        {"name": f"%{name}%"},
    )
    courses = query.fetchall()
    return courses


# find singular course by id
def find_by_id(course_id: str):
    query = make_query(
        "SELECT * FROM courses WHERE id = :course_id", {"course_id": course_id}
    )
    return query.fetchone()
