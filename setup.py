"""Setup chunknorris module"""

from setuptools import setup

from chunknorris import __version__

setup(
    name="chunknorris",
    version=__version__,
    py_modules=["chunknorris"],
    install_requires=["typer[all]"],
    entry_points={"console_scripts": ["chunknorris = chunknorris.main:app"]},
)
