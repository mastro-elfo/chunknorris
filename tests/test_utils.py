# pylint: disable=missing-module-docstring

import os
import re
import string

from chunknorris.utils import get_output_filename, remove_white_spaces, split_extension


# pylint: disable=missing-function-docstring
def test_split_extension():
    name, ext = split_extension("test.file.name.ext")
    assert name == "test.file.name"
    assert ext == "ext"


# pylint: disable=missing-function-docstring
def test_get_output_filename():
    assert (
        get_output_filename(
            "basename", "txt", extra="output", separator="_", output_dir="output-dir"
        )
        == f"output-dir{os.sep}basename_output.txt"
    )
    assert re.match(
        r"basename.output\.txt", get_output_filename("basename", "txt", extra="output")
    )
    assert get_output_filename("basename", "txt", separator="_") == "basename.txt"
    assert (
        get_output_filename("basename", "txt", output_dir="output-dir")
        == f"output-dir{os.sep}basename.txt"
    )


def test_all_white_spaces_removed():
    assert (
        remove_white_spaces(
            "\r\n\t ",
            carriage_return=True,
            line_feed=True,
            tab=True,
            space=True,
            strip=True,
        )
        == ""
    )


def test_carriage_return_is_kept():
    assert (
        remove_white_spaces(
            "\r\n\t ",
            carriage_return=False,
            line_feed=True,
            tab=True,
            space=True,
            strip=False,
        )
        == "\r "
    )


def test_line_feed_is_kept():
    assert (
        remove_white_spaces(
            "\r\n\t ",
            carriage_return=True,
            line_feed=False,
            tab=True,
            space=True,
            strip=False,
        )
        == " \n "
    )


def test_tab_is_kept():
    assert (
        remove_white_spaces(
            "\r\n\t ",
            carriage_return=True,
            line_feed=True,
            tab=False,
            space=True,
            strip=False,
        )
        == " \t "
    )


def test_space_is_kept():
    assert (
        remove_white_spaces(
            "\r\n\t ",
            carriage_return=True,
            line_feed=True,
            tab=True,
            space=False,
            strip=False,
        )
        == "  "
    )


def test_non_spaces_are_kept():
    assert (
        remove_white_spaces(
            string.ascii_letters + string.digits + string.punctuation,
            carriage_return=True,
            line_feed=True,
            tab=True,
            space=True,
            strip=True,
        )
        == string.ascii_letters + string.digits + string.punctuation
    )
