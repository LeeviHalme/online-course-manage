from flask import Blueprint, render_template, request, redirect, session
from modules.auth import try_login, get_user_by_email, create_user
from modules.db import serialize_to_dict

auth = Blueprint("auth", __name__, url_prefix="/auth")

# app login page
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    # get request body
    email = request.form["email"]
    password = request.form["password"]

    # try logging in
    success = try_login(email, password)

    # if email or password were wrong
    if not success:
        return render_template(
            "login.html", alert=("danger", "Invalid E-mail Address or Password")
        )

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
    name = request.form["name"]
    email = request.form["email"]
    userType = request.form["userType"]
    password = request.form["password"]
    passwordConfirm = request.form["passwordConfirm"]

    # check if passwords won't match
    if password != passwordConfirm:
        return render_template(
            "register.html",
            alert=("danger", "Passwords won't match!"),
        )

    # TODO: Add validation

    # check if user already exists
    user = get_user_by_email(email)
    if user:
        return render_template(
            "register.html",
            alert=("danger", "User with this E-mail Address already exists!"),
        )

    # create new user
    create_user(name, email, password, userType)

    # Add session
    user = get_user_by_email(email)
    session["user"] = serialize_to_dict(user)

    return redirect("/courses")


# app logout handler
@auth.route("/logout", methods=["GET"])
def logout():
    del session["user"]
    return redirect("/")
