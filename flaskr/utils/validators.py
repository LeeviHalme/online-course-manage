# Collection of simple validators
import re


# Validate E-Mail addresses
# Source: https://stackabuse.com/python-validate-email-address-with-regular-expressions-regex/
def email(input: str) -> bool:
    regex = re.compile(
        r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
    )
    return bool(re.fullmatch(regex, input))


# Validate booleans
def boolean(input: str) -> bool:
    if input == "on":
        return True
    else:
        return False


# Validate alphabetic strings
def alpha(input: str) -> bool:
    return input.isalpha()


# Validate password (>= 5 characters)
def password(input: str) -> bool:
    return len(input) >= 5


# Validate SQL USER_TYPE
def user_type(input: str) -> bool:
    if input == "STUDENT":
        return True
    elif input == "TEACHER":
        return True
    else:
        return False


# Validate SQL QUESTION_TYPE
def question_type(input: str) -> bool:
    if input == "MULTICHOISE":
        return True
    elif input == "OPEN":
        return True
    else:
        return False


# validate answers array from creating an exercise
def answers_array(input: str) -> bool:
    answers = input.split(";")
    valid = True

    # if less than 2 answers
    if len(answers) < 2:
        return False

    # check each answer
    for answer in answers:
        content, is_correct = answer.split(",")

        # if there is no content
        if len(content) == 0:
            valid = False

        # if is_correct is not a boolean
        elif is_correct != "true" and is_correct != "false":
            valid = False

    return valid


# parse answers array from creating a exercise
def parse_answers_array(input: str) -> list:
    answers = input.split(";")
    to_return = []

    # check each answer
    for answer in answers:
        content, is_correct = answer.split(",")
        to_return.append(
            {"answer": content, "correct": True if is_correct == "true" else False}
        )

    return to_return
