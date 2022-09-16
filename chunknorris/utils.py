# pylint: disable=missing-module-docstring

import locale
import os
import re
from io import TextIOWrapper
from typing import Optional


def split_extension(filename: str) -> tuple[str, str]:
    """Split filename and file extension"""

    basename = os.path.basename(filename)
    *parts, extension = basename.split(".")
    return ".".join(parts), extension


def get_output_filename(
    basename: str,
    extension: str,
    output_dir: str = "",
    extra: int | str = "",
    separator: str = "-",
) -> str:
    """Get output filename"""

    return os.path.join(
        output_dir, f"{basename}{separator if extra else ''}{extra}.{extension}"
    )


def open_writer(
    basename: str,
    count: int,
    extension: str,
    separator: str = "-",
    output_dir: str = "",
    header: str = "",
) -> TextIOWrapper:
    """Open file and write header"""

    writer = open(
        get_output_filename(output_dir, basename, separator, count, extension),
        "w",
        encoding=locale.getpreferredencoding(),
    )
    writer.write(header)
    return writer


def close_writer(writer: TextIOWrapper, footer: str = ""):
    """Write footer and close file"""

    writer.write(footer if footer else "")
    writer.close()


def remove_white_spaces(
    input_str: str,
    carriage_return: Optional[bool] = True,
    line_feed: Optional[bool] = True,
    tab: Optional[bool] = True,
    space: Optional[bool] = True,
    strip: Optional[bool] = True,
) -> str:
    """Remove white spaces from input string"""

    pattern = (
        (r"\r" if carriage_return else "")
        + (r"\n" if line_feed else "")
        + (r"\t" if tab else "")
        + (r"\ " if space else "")
    )

    regex: re.Pattern[str] = re.compile(r"[" + pattern + "]+")
    output_str: str = re.sub(regex, " ", input_str)
    if strip:
        output_str = output_str.strip()
    return output_str
