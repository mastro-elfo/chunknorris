from importlib.metadata import entry_points
from setuptools import setup

setup(
    name="chunknorris",
    version="0.1",
    py_modules=["chunknorris"],
    install_requires=["Click"],
    entry_points="""
        [console_scripts]
        chunknorris=cli:main
    """,
)
