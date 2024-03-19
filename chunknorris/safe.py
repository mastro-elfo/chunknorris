"""Encrypt and decrypt files with password"""

import typer

from chunknorris import encryption

app = typer.Typer()


@app.command()
def encrypt(
    input_file: typer.FileBinaryRead,
    output_file: typer.FileBinaryWrite,
    password: str = typer.Option(
        "", prompt="Enter encryption password", hide_input=True
    ),
):
    """Encrypt file with password"""
    if password:
        output_file.write(encryption.encrypt(input_file.read(), password))


@app.command()
def decrypt(
    input_file: typer.FileBinaryRead,
    output_file: typer.FileBinaryWrite,
    password: str = typer.Option(
        "", prompt="Enter decryption password", hide_input=True
    ),
):
    """Decrypt file with password"""

    try:
        output_file.write(encryption.decrypt(input_file.read(), password))

    except encryption.DecryptionError as error:
        print(error)
