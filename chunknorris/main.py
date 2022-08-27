from io import TextIOWrapper
import os
from typing import Optional
import typer
import rich

app = typer.Typer()


def split_extension(filename: str) -> tuple[str, str]:
    basename = os.path.basename(filename)
    *parts, extension = basename.split(".")
    return ".".join(parts), extension


def open_writer(
    basename: str,
    count: int,
    extension: str,
    separator: str = "-",
    output_dir: str = "",
    header: str = "",
) -> TextIOWrapper:
    writer = open(
        os.path.join(output_dir, f"{basename}{separator}{count}.{extension}"), "w"
    )
    writer.write(header)
    return writer


def close_writer(writer: TextIOWrapper, footer: str = ""):
    writer.write(footer)
    writer.close()


@app.command()
def main(
    input_file: typer.FileText,
    breaking_line: str,
    occurrences: int,
    header: Optional[str] = typer.Option("-", "--header", "-h"),
    header_file: Optional[typer.FileText] = typer.Option(None, "--header-file", "-hf"),
    footer: Optional[str] = typer.Option("", "--footer", "-f"),
    footer_file: Optional[typer.FileText] = typer.Option(None, "--footer-file", "-ff"),
    index: Optional[int] = typer.Option(1, "--index", "-i"),
    separator: Optional[str] = typer.Option("-", "--separator", "-s"),
    output_dir: Optional[str] = typer.Option("", "--output-dir", "-od"),
):
    header_content = header_file.read() if header_file else header
    footer_content = footer_file.read() if footer_file else footer

    count_occurrences = 0
    file_index = index
    basename, extension = split_extension(input_file.name)

    writer_factory = lambda: open_writer(
        basename, file_index, extension, separator, output_dir, header_content
    )

    writer = writer_factory()

    for line in input_file:
        writer.write(line)

        if line.find(breaking_line) != -1:
            count_occurrences += 1

        if count_occurrences == occurrences:
            close_writer(writer, footer_content)
            count_occurrences = 0
            file_index += 1
            writer = writer_factory()

    close_writer(writer)

    rich.print("[green]Done![/green]")
