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


# create new submission and return it's id
def create_submission(
    question_id: str, question_type: str, user_id: str, answer_id: str, open_answer: str
) -> str:
    # if multichoise question
    if question_type == "MULTICHOISE":
        params = {
            "question_id": question_id,
            "user_id": user_id,
            "answer_id": answer_id,
        }
        text_query = """
        INSERT INTO submissions (id, question_id, user_id, answer_id)
        VALUES (
            gen_random_uuid(),
            :question_id,
            :user_id,
            :answer_id
        )
        RETURNING submissions.id
        """
        result = make_insert(text_query, params)
        returned_values = result.mappings().first()
        inserted_id = returned_values.get("id")
        return inserted_id
    # if open question (essay)
    elif question_type == "OPEN":
        params = {
            "question_id": question_id,
            "user_id": user_id,
            "open_answer": open_answer,
        }
        text_query = """
        INSERT INTO submissions (id, question_id, user_id, open_answer)
        VALUES (
            gen_random_uuid(),
            :question_id,
            :user_id,
            :open_answer
        )
        RETURNING submissions.id
        """
        result = make_insert(text_query, params)
        returned_values = result.mappings().first()
        inserted_id = returned_values.get("id")
        return inserted_id


# get answer by id
def get_answer(answer_id: str):
    # query for answer existence
    query = make_query(
        "SELECT id, question_id, answer, correct FROM exercise_answers WHERE id = :answer_id",
        {"answer_id": answer_id},
    )
    return query.fetchone()


# get user submissions for all courses
def get_user_submissions(user_id: str):
    # query for user submissions
    text_query = """
    SELECT
      S.id,
      S.user_id,
      Q.id,
      Q.question,
      Q.type,
      Q.points,
      A.points,
      C.name,
      S.created_at
    FROM submissions S
    
    LEFT JOIN exercise_questions Q
    ON S.question_id = Q.id

    LEFT JOIN courses C
    ON Q.course_id = C.id

    LEFT JOIN awarded_points A
    ON S.id = A.submission_id

    GROUP BY
      S.id,
      S.user_id,
      Q.id,
      Q.question,
      Q.type,
      Q.points,
      A.points,
      C.name,
      S.created_at

    HAVING S.user_id = :user_id
    """
    query = make_query(text_query, {"user_id": user_id})
    rows = query.fetchall()
    to_return = []

    # format rows
    for row in rows:
        (
            submission_id,
            submission_user_id,
            question_id,
            question_name,
            question_type,
            max_points,
            awarded_points,
            course_name,
            created_at,
        ) = row
        to_return.append(
            {
                "submission_id": submission_id,
                "user_id": submission_user_id,
                "question_id": question_id,
                "question_name": f"{question_name[:25]}..."
                if len(question_name) > 25
                else question_name,
                "question_type": question_type,
                "max_points": max_points,
                "awarded_points": awarded_points,
                "course_name": course_name,
                "created_at": created_at,
            }
        )

    return sorted(to_return, key=lambda s: s["created_at"], reverse=True)


# add points to submission
def grade_submission(submission_id: str, points: int, comment: str):
    text_query = """
    INSERT INTO awarded_points (submission_id, points, comment)
    VALUES (
        :submission_id,
        :points,
        :comment
    )
    """
    params = {"submission_id": submission_id, "points": points, "comment": comment}
    make_insert(text_query, params)
