from collections import UserString
from io import IOBase
from os import PathLike
import random
import string
from typing import Any, Iterable, Mapping
import datetime

TRUE_STRINGS = {"TRUE", "YES", "ON", "1"}
FALSE_STRINGS = {"FALSE", "NO", "OFF", "0", "NONE", ""}


def get_alpha_numeric(self, length, type="letters"):
    alpha_num = ""
    if type == "digits":
        case = string.digits
    elif type == "lower":
        case = string.ascii_lowercase
    elif type == "mix":
        case = string.ascii_letters + string.digits
    elif type == "upper":
        case = string.ascii_uppercase
    else:
        case = string.ascii_letters
    return alpha_num.join(random.choice(case) for _ in range(length))


def get_unique_name(self, char_count=10):
    return self.get_alpha_numeric(char_count, "lower")


def get_unique_name_list(self, list_size=5, item_length=None):
    return [self.getUniqueName(item_length[i]) for i in range(list_size)]


def verify_list_match(self, expected, actual):
    return set(expected) == set(actual)


def verify_list_contains(self, expected, actual):
    length = len(expected)
    return all(expected[i] in actual for i in range(length))


def verify_text_contains(self, actual, expected):
    return expected.lower() in actual.lower()


def verify_text_match(self, actual, expected):
    return expected.lower() == actual.lower()


def plural_or_not(item):
    count = item if is_integer(item) else len(item)
    return "" if count in (1, -1) else "s"


def is_integer(item):
    return isinstance(item, int)


def is_number(item):
    return isinstance(item, (int, float))


def is_bytes(item):
    return isinstance(item, (bytes, bytearray))


def is_string(item):
    return isinstance(item, str)


def is_pathlike(item):
    return isinstance(item, PathLike)


def is_list_like(item):
    if isinstance(item, (str, bytes, bytearray, UserString, IOBase)):
        return False
    return isinstance(item, Iterable)


def is_dict_like(item):
    return isinstance(item, Mapping)


def type_converter(argument: Any) -> str:
    return type(argument).__name__.lower()


def generate_random_email_and_password(domain=None, email_prefix=None):
    if not domain:
        domain = "takealot.com"
    if not email_prefix:
        email_prefix = "test_user"

    temp_length = 10
    random_string = "".join(random.choices(string.ascii_lowercase, k=temp_length))
    generated_email = f"{email_prefix}_{random_string}@{domain}"

    temp_length = 20
    generated_password = "".join(random.choices(string.ascii_lowercase, k=temp_length))
    return {"email": generated_email, "password": generated_password}


def generate_random_string(length=10, prefix=None, suffix=None):
    random_string = "".join(random.choices(string.ascii_lowercase, k=length))

    if prefix:
        random_string = prefix + random_string
    if suffix:
        random_string += suffix

    return random_string


def get_datetime_string():
    """Getting a date string to use for naming files"""
    return datetime.datetime.now().strftime("%y%m%d%H%M%S")
