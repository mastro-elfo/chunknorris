# pylint: disable=missing-module-docstring

import os
import re

from chunknorris.utils import get_output_filename, split_extension


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
