from multiprocessing.sharedctypes import Value
from pathlib import Path
from termios import VLNEXT

import yaml
from pytest import raises
from sourcelib.collect import NoSourceFilesInFolderError, NonExistentModeInYamlSource

from .testfiles.testclasses import DocumentCollector, DocumentFile


def test_collect_by_path():
    path = Path(__file__).parent / "testfiles" / "testparts" / "p1.txt"
    documents = DocumentCollector.get_files_from_path("doc", "default", path)
    assert len(documents) == 1
    assert isinstance(documents[0], DocumentFile)

def test_collect_by_folder():
    folder = Path(__file__).parent / "testfiles" / "testparts"
    documents = DocumentCollector.get_files_from_folder("doc", folder, "default")
    assert len(documents) == 2

def test_collect_by_folder_no_files():
    with raises(NoSourceFilesInFolderError) as errors:
        folder = Path(__file__).parent
        _ = DocumentCollector.get_files_from_folder("doc", folder, "default")

def test_collect_by_filter():
    folder = Path(__file__).parent / "testfiles" / "testparts"
    documents = DocumentCollector.get_files_from_folder(
        "doc", folder, "default", filters=("1",)
    )
    assert len(documents) == 1
    assert documents[0].path == (folder / "p1.txt")


def test_collect_by_excludes():
    folder = Path(__file__).parent / "testfiles" / "testparts"
    documents = DocumentCollector.get_files_from_folder(
        "doc", folder, "default", excludes=("1",)
    )
    assert len(documents) == 1
    assert documents[0].path == (folder / "p2.txt")


def test_collect_from_yaml():
    yaml_path = Path(__file__).parent / "testfiles" / "data.yml"
    documents = DocumentCollector.get_files_from_yaml("doc", yaml_source=yaml_path)
    assert len(documents) == 1
    assert str(documents[0].path) == "/home/mart/code/source-lib/tests/testfiles/test.md"


def test_collect_from_yaml_source():
    yaml_path = Path(__file__).parent / "testfiles" / "data.yml"
    with open(yaml_path) as file:
        yaml_source = yaml.load(file, Loader=yaml.FullLoader)
    documents = DocumentCollector.get_files_from_yaml("doc", yaml_source=yaml_source)
    assert len(documents) == 1
    assert str(documents[0].path) == "/home/mart/code/source-lib/tests/testfiles/test.md"


def test_collect_from_yaml_source_error_mode():
    with raises(NonExistentModeInYamlSource) as errors:
        yaml_path = Path(__file__).parent / "testfiles" / "data.yml"
        _ = DocumentCollector.get_files_from_yaml("doc", yaml_source=yaml_path, mode='nomode')
