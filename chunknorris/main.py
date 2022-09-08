"""Perform actions on files"""

import locale
import os
from typing import Optional

import rich
import typer

from chunknorris.utils import close_writer, open_writer, split_extension

app = typer.Typer()


@app.command()
def chunk(
    input_file: typer.FileText,
    breaking_line: str,
    occurrences: int,
    header: str = typer.Option("", "--header", "-h"),
    header_file: Optional[typer.FileText] = typer.Option(None, "--header-file", "-hf"),
    footer: str = typer.Option("", "--footer", "-f"),
    footer_file: Optional[typer.FileText] = typer.Option(None, "--footer-file", "-ff"),
    index: int = typer.Option(1, "--index", "-i"),
    separator: str = typer.Option("-", "--separator", "-s"),
    output_dir: str = typer.Option("", "--output-dir", "-od"),
):
    """Splits text file in chunks"""

    header_content = header_file.read() if header_file else header
    footer_content = footer_file.read() if footer_file else footer

    count_occurrences = 0
    file_index = index if index is not None else 1
    basename, extension = split_extension(input_file.name)

    def writer_factory():
        return open_writer(
            basename,
            file_index,
            extension,
            separator,
            output_dir,
            header_content,
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


@app.command()
# pylint: disable=redefined-builtin
def filter(
    input_file: typer.FileText,
    block_tag: str,
    tag: str,
    value: str,
    separator: Optional[str] = typer.Option("_", "--separator", "-s"),
    output_dir: Optional[str] = typer.Option("", "--output-dir", "-od"),
):
    """Filter XML block"""

    basename, extension = split_extension(input_file.name)

    with open(
        os.path.join(
            output_dir if output_dir else "",
            f"{basename}{separator}{value}.{extension}",
        ),
        "w",
        encoding=locale.getpreferredencoding(),
    ) as writer:
        buffer: str = ""
        open_block_tag = f"<{block_tag}>"
        close_block_tag = f"</{block_tag}>"
        open_tag = f"<{tag}>"
        match_value = False
        in_block = False
        for line in input_file:
            if open_block_tag in line:
                buffer = line
                in_block = True
            elif close_block_tag in line:
                if match_value:
                    buffer += line
                    writer.write(buffer)
                buffer = ""
                in_block = False
            elif open_tag in line:
                buffer += line
                match_value = value in line
            elif not in_block:
                writer.write(line)
            else:
                buffer += line


if __name__ == "__main__":
    app()
