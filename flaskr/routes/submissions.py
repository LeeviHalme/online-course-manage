from flask import Blueprint, render_template, abort, redirect, session, request, flash
from modules.courses import find_by_id, is_enrolled
from modules.submissions import (
    get_submission,
    get_question,
    get_answer,
    create_submission,
)

submissions = Blueprint("submissions", __name__, url_prefix="/submissions")


# create new submission route
@submissions.route("/new", methods=["POST"])
def new_submission():
    # if user is not logged in
    user = session.get("user")
    if not user:
        return abort(401)

    # get request body
    values = request.form
    course_id = values.get("course_id")
    question_id = values.get("question_id")
    answer_id = values.get("answer_id")
    open_answer = values.get("open_answer")

    # if course doesn't exist
    course = find_by_id(course_id)
    if not course:
        return abort(404)

    # check that user participates
    enrolled = is_enrolled(course_id, user["id"])
    if not enrolled:
        return abort(403)

    # Validate UID's
    question = get_question(question_id)
    answer = get_answer(answer_id)
    if not question:
        return abort(400)

    # if answering a multichoise-question
    if question.type == "MULTICHOISE":
        # if answer_id not provided or is malformed
        if not answer:
            return abort(400)
        elif answer.question_id != question.id:
            return abort(400)
    # if answering a open question and no answer provided
    elif question.type == "OPEN":
        # if open answer not provided or is malformed
        if not open_answer:
            return abort(400)

    # check if user already has a submission
    # for this exercise
    submission = get_submission(question_id, user["id"])
    if submission:
        return abort(403)

    # create new submission
    create_submission(question_id, question.type, user["id"], answer_id, open_answer)

    flash("Success! Answer to the question saved.", "success")

    return redirect(f"/courses/{course_id}/exercises")
