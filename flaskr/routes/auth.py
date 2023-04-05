from flask import Blueprint, render_template

auth = Blueprint("auth", __name__, url_prefix="/auth")

# app login page
@auth.route("/login")
def login():
    return render_template("login.html")


# app register page
@auth.route("/register")
def register():
    return render_template("register.html")
