from io import TextIOWrapper
import os


def split_extension(filename: str) -> tuple[str, str]:
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
    writer = open(
        get_output_filename(output_dir, basename, separator, count, extension), "w"
    )
    writer.write(header)
    return writer


def close_writer(writer: TextIOWrapper, footer: str = ""):
    writer.write(footer)
    writer.close()
