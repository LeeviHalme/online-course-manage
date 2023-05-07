from modules.db import make_query, make_insert
from modules.courses import get_course_exercises


# get user submission for a exercise
def get_submission(question_id: str, user_id: str):
    # query for submission existence
    query = make_query(
        "SELECT created_at FROM submissions WHERE question_id = :question_id AND user_id = :user_id",
        {"question_id": question_id, "user_id": user_id},
    )
    submission = query.fetchone()
    return submission


# get user completed exercise UID list
def get_completed_exercises(course_id: str, user_id: str) -> list:
    exercises = get_course_exercises(course_id)
    to_return = []

    # loop through exercises and check if user has
    # completed them
    for exercise in exercises:
        submission = get_submission(exercise["id"], user_id)
        # if user has submission
        if submission:
            to_return.append(exercise["id"])

    return to_return


# get question by id
def get_question(question_id: str):
    # query for question existence
    query = make_query(
        "SELECT id, course_id, question, points, type FROM exercise_questions WHERE id = :question_id",
        {"question_id": question_id},
    )
    return query.fetchone()


# create new submission
def create_submission(
    question_id: str, question_type: str, user_id: str, answer_id: str, open_answer: str
):
    # if multichoise question
    if question_type == "MULTICHOISE":
        params = {
            "question_id": question_id,
            "user_id": user_id,
            "answer_id": answer_id,
        }
        text_query = """
        INSERT INTO submissions (question_id, user_id, answer_id)
        VALUES (
            :question_id,
            :user_id,
            :answer_id
        )
        """
        make_insert(text_query, params)
    # if open question (essay)
    elif question_type == "OPEN":
        params = {
            "question_id": question_id,
            "user_id": user_id,
            "open_answer": open_answer,
        }
        text_query = """
        INSERT INTO submissions (question_id, user_id, open_answer)
        VALUES (
            :question_id,
            :user_id,
            :open_answer
        )
        """
        make_insert(text_query, params)


# get answer by id
def get_answer(answer_id: str):
    # query for answer existence
    query = make_query(
        "SELECT id, question_id, answer, correct FROM exercise_answers WHERE id = :answer_id",
        {"answer_id": answer_id},
    )
    return query.fetchone()
