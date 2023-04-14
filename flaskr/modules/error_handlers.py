from flask import render_template


# Handler for 404 errors
# 404 - Not Found
def not_found(error):
    return render_template("not_found.html"), 404


# Handler for 401 errors
# 401 - Unauthorized
def unauthorized(error):
    return render_template("unauthorized.html"), 401


# Handler for 403 errors
# 403 - Forbidden
def forbidden(error):
    return render_template("forbidden.html"), 403
