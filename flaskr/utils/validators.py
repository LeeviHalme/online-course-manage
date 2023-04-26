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
def user_type(input: str):
    if input == "STUDENT":
        return True
    elif input == "TEACHER":
        return True
    else:
        return False
