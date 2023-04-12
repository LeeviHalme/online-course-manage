from flask import Blueprint, render_template

main = Blueprint("main", __name__)


# app homepage route
@main.route("/")
def index():
    # project github link
    gh_link = "https://github.com/LeeviHalme/online-course-manager"

    return render_template("home.html", gh_link=gh_link)
