from modules.db import make_query, make_insert
from werkzeug.security import check_password_hash, generate_password_hash


# try to login using given credentials
# returns success flag as boolean
def try_login(email: str, password: str) -> bool:
    # query for user existence
    query = make_query(
        "SELECT password_hash FROM users WHERE email = :email", {"email": email}
    )
    result = query.fetchone()

    # if email was incorrect
    if not result:
        return False

    # validate password
    valid_password = check_password_hash(result[0], password)

    # if password was incorrect
    if not valid_password:
        return False

    return True


# creates a new user and returns their UUID
def create_user(name: str, email: str, password: str, userType: str) -> str:
    # create password hash
    password_hash = generate_password_hash(password)

    # insert user into database
    params = {
        "name": name,
        "email": email,
        "userType": userType,
        "password_hash": password_hash,
    }
    text_query = "INSERT INTO users (id, name, email, type, password_hash) VALUES (gen_random_uuid(), :name, :email, :userType, :password_hash)"
    make_insert(text_query, params)

    # get just created user
    user = get_user_by_email(email)

    # return new user's uuid
    return user[0]


# get user using email address
def get_user_by_email(email: str):
    # query for user existence
    query = make_query(
        "SELECT id, name, email, type FROM users WHERE email = :email", {"email": email}
    )
    user = query.fetchone()
    return user


# get user using uuid
def get_user_by_id(id: str):
    # query for user existence
    query = make_query(
        "SELECT id, name, email, type FROM users WHERE id = :id", {"id": id}
    )
    user = query.fetchone()
    return user
