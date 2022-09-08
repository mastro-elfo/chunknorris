# pylint: disable=missing-module-docstring

import locale
import os
from io import TextIOWrapper


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
