from chunknorris.utils import split_extension


def test_split_extension():
    name, ext = split_extension("test.file.name.ext")
    assert name == "test.file.name"
    assert ext == "ext"
