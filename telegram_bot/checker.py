"""This module provides functional for checking equality of text files"""


def get_text(file_name):
    with open(file_name, "rb") as inp:
        text = inp.readlines()
    return text


def files_equal(file_name_a, file_name_b):
    text_a = get_text(file_name_a)
    text_b = get_text(file_name_b)

    return text_a == text_b
