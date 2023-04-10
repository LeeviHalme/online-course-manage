from modules.db import make_query, make_insert, serialize_to_dict

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


# check if user is a participant on a course
# returns boolean status flag
def is_enrolled(course_id: str, user_id: str):
    params = {"course_id": course_id, "user_id": user_id}
    query = make_query(
        "SELECT 1 from participants WHERE user_id = :user_id AND course_id = :course_id",
        params,
    )
    result = query.fetchone()

    if result:
        return True
    else:
        return False


# validate invitation code
# returns boolean status flag
def validate_invitation_code(course_id: str, code: str):
    result = find_by_id(course_id)

    # if course_id was invalid
    if not result:
        return False

    # if code was invalid
    course = serialize_to_dict(result)

    print(course["invitation_code"])

    if course["invitation_code"] != code:
        return False
    else:
        return True


# create a new participant record
def enroll_to_course(course_id: str, user_id: str):
    # insert user into database
    params = {
        "user_id": user_id,
        "course_id": course_id,
    }
    text_query = (
        "INSERT INTO participants (user_id, course_id) VALUES (:user_id, :course_id)"
    )
    make_insert(text_query, params)
