from modules.db import make_query


# get user enrolled courses
# returns array of courses
def get_enrolled_courses(user_id: str):
    args = {"user_id": user_id}
    query = "SELECT C.id, C.name, C.short_description, P.created_at FROM courses C LEFT JOIN participants P ON P.course_id = C.id WHERE P.user_id = :user_id"
    result = make_query(query, args)
    courses = result.fetchall()

    return courses
