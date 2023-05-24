import re

def is_password_valid(password):
    # define password policy
    pw_length = range(8, 21)
    has_lowercase = re.search(r"[a-z]", password)
    has_digit = re.search(r"\d", password)

    # check if password meets policy requirements
    if len(password) not in pw_length:
        return False
    if not has_lowercase or not has_digit:
        return False

    return True