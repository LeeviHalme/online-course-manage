from flask import Blueprint, render_template, request, redirect, session, flash
from modules.auth import try_login, get_user_by_email, create_user
from modules.db import serialize_to_dict
import utils.validators as validate

auth = Blueprint("auth", __name__, url_prefix="/auth")


# app login page
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    # get request body
    email = request.form["email"]
    password = request.form["password"]

    # Validate email
    if not validate.email(email):
        flash("Malformed email address!", "danger")
        return redirect(request.url)

    # try logging in
    success = try_login(email, password)

    # if email or password were wrong
    if not success:
        flash("Invalid E-mail Address or Password", "danger")
        return redirect(request.url)

    # Add session
    user = get_user_by_email(email)
    session["user"] = serialize_to_dict(user)

    return redirect("/courses")


# app register page
@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    # get request body
    values = request.form
    name = values.get("name")
    email = values.get("email")
    user_type = values.get("userType")
    password = values.get("password")
    password_confirm = values.get("passwordConfirm")

    # Validate name (alphabetic, 5-50 chars)
    if len(name) < 5 or len(name) > 50:
        flash("Invalid name! 5-50 characters.", "danger")
        return redirect(request.url)

    # Validate email
    elif not validate.email(email):
        flash("Invalid email address!", "danger")
        return redirect(request.url)

    # Validate userType (either 'TEACHER' or 'STUDENT')
    elif not validate.user_type(user_type):
        flash("Please choose your user type!", "danger")
        return redirect(request.url)

    # validate password (alphanumeric and >= 5 characters)
    elif not validate.password(password):
        flash("Invalid password! At least 5 characters (a-Z, 0-9)", "danger")
        return redirect(request.url)

    # check if passwords won't match
    elif password != password_confirm:
        flash("Passwords won't match!", "danger")
        return redirect(request.url)

    # check if user already exists
    user = get_user_by_email(email)
    if user:
        flash("User with this E-mail Address already exists!", "danger")
        return redirect(request.url)

    # create new user
    create_user(name, email, password, user_type)

    # Add session
    user = get_user_by_email(email)
    session["user"] = serialize_to_dict(user)

    return redirect("/courses")


# app logout handler
@auth.route("/logout", methods=["GET"])
def logout():
    del session["user"]
    flash("Successfully logged out!", "success")
    return redirect("/")
