from modules.db import make_query
import utils.validators as validate


# get user enrolled courses
# returns array of courses
def get_enrolled_courses(user_id: str):
    args = {"user_id": user_id}
    query = "SELECT C.id, C.name, C.short_description, P.created_at FROM courses C LEFT JOIN participants P ON P.course_id = C.id WHERE P.user_id = :user_id"
    result = make_query(query, args)
    courses = result.fetchall()

    return courses


# validates a list of email addresses
# checks that they exist and have correct type
def validate_email_list(type: str, emails: list) -> bool:
    # validate type
    if not validate.user_type(type):
        return False

    # store success flag
    success = True

    # loop through array
    for email in emails:
        args = {"email": email, "type": type}
        query = "SELECT id FROM users WHERE email = :email AND type = :type"
        result = make_query(query, args)
        user = result.fetchone()

        if not user:
            success = False

    return success
