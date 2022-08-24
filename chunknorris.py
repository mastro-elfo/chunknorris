from io import TextIOWrapper
import os
import click


class BaseError(Exception):
    def __init__(self, message: str, *args: object) -> None:
        self.message = message
        super().__init__(*args)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.message}"


def read_file_content(filename: str) -> str:
    try:
        with open(filename, "r") as fp:
            return fp.read()
    except FileNotFoundError:
        raise BaseError(f"File not found: {filename}")


def split_extension(filename: str) -> tuple[str, str]:
    basename = os.path.basename(filename)
    *parts, extension = basename.split(".")
    return ".".join(parts), extension


def get_output_filename(
    basename: str,
    count: int,
    extension: str,
    separator: str = "-",
    output_dir: str = "",
) -> str:
    return os.path.join(output_dir, f"{basename}{separator}{count}.{extension}")


def open_writer(filename: str, header: str = "") -> TextIOWrapper:
    try:
        writer = open(filename, "w")
        writer.write(header)
        return writer
    except FileNotFoundError:
        raise BaseError(f"File not found: {filename}; Output directory must exists.")
    except PermissionError:
        raise BaseError(f"Permission to write denied for {filename}")


def close_writer(writer: TextIOWrapper, footer: str = ""):
    writer.write(footer)
    writer.close()


def open_reader(filename: str) -> TextIOWrapper:
    try:
        return open(filename, "r")
    except FileNotFoundError:
        raise BaseError(f"File not found: {filename}")
    except PermissionError:
        raise BaseError(f"Permission to read denied for {filename}")


def close_reader(reader: TextIOWrapper):
    reader.close()


def warning(message: str):
    click.echo(click.style(message, bg="yellow"))


def error(message: str):
    click.echo(click.style(message, bg="red"))


@click.command()
@click.argument("input-file")
@click.argument("breaking-line")
@click.argument("occurrences", type=int)
@click.option("--header", "-h", default="", help="Header part")
@click.option(
    "--header-file",
    "-hf",
    default=None,
    help="Filename which contains the header part, if given overwrites --header",
)
@click.option("--footer", "-f", default="", help="Footer part")
@click.option(
    "--footer-file",
    "-ff",
    default=None,
    help="Filename which contains the footer part, if given overwrites --footer",
)
@click.option(
    "--index", "-i", type=int, default=1, help="Start value for incrementing index"
)
@click.option(
    "--separator",
    "-s",
    default="-",
    help="Separate the output filename from the incrementing index",
)
@click.option(
    "--output-dir", "-od", default="", help="Output directory, defaults to current"
)
def cli(
    input_file: str,
    breaking_line: str,
    occurrences: int,
    header_file: str,
    footer_file: str,
    header: str,
    footer: str,
    index: int,
    separator: str,
    output_dir: str,
):
    """Splits file in chunks

    INPUT_FILE is the file to read
    BREAKING_LINE is searched while reading the file
    OCCURRENCES is the maximum number of BREAKING_LINE after which the file is split in chunk"""

    if occurrences < 1:
        warning("Occurrences is less than 1")

    header_content = (
        read_file_content(header_file) if header_file else f"{header}{os.linesep}"
    )
    footer_content = (
        read_file_content(footer_file) if footer_file else f"{footer}{os.linesep}"
    )
    count_occurrences = 0
    file_index = index
    basename, extension = split_extension(input_file)
    reader = open_reader(input_file)
    writer = open_writer(
        get_output_filename(basename, file_index, extension, separator, output_dir)
    )

    while line := reader.readline():
        writer.write(line)

        if line.find(breaking_line) != -1:
            count_occurrences += 1

        if count_occurrences == occurrences:
            close_writer(writer, footer_content)
            count_occurrences = 0
            file_index += 1
            writer = open_writer(
                get_output_filename(
                    basename, file_index, extension, separator, output_dir
                ),
                header_content,
            )

    close_writer(writer)
    close_reader(reader)


def main():
    try:
        cli()
    except BaseError as e:
        error(e)


if __name__ == "__main__":
    main()
