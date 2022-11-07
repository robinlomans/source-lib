from pathlib import Path
from telnetlib import DO

import yaml
from pytest import raises
from sourcelib.collect import (
    NonExistentModeInYamlSource,
    NoSourceFilesInFolderError,
    get_files_from_folder,
    get_files_from_path,
    get_files_from_yaml,
)
from sourcelib.file import FileMode

from .testfiles.testclasses import DocumentFileMode, DocumentFile


def test_collect_by_path():
    path = Path(__file__).parent / "testfiles" / "testparts" / "p1.txt"
    documents = get_files_from_path(
        file_cls=DocumentFile,
        mode=FileMode.default,
        path=path,
    )
    assert len(documents) == 1
    assert isinstance(documents[0], DocumentFile)


def test_collect_by_folder():
    folder = Path(__file__).parent / "testfiles" / "testparts"
    documents = get_files_from_folder(
        folder=folder,
        file_cls=DocumentFile,      
    )
    assert len(documents) == 2


def test_collect_by_folder_no_files():
    with raises(NoSourceFilesInFolderError):
        folder = Path(__file__).parent
        _ = get_files_from_folder(
            file_cls=DocumentFile,
            folder=folder,
        )


def test_collect_by_filter():
    folder = Path(__file__).parent / "testfiles" / "testparts"
    documents = get_files_from_folder(
        file_cls=DocumentFile, folder=folder, filters="1", 
    )
    assert len(documents) == 1
    assert documents[0].path == (folder / "p1.txt")


def test_collect_by_excludes():
    folder = Path(__file__).parent / "testfiles" / "testparts"
    documents = get_files_from_folder(
        file_cls=DocumentFile, folder=folder, excludes="1"
    )
    assert len(documents) == 1
    assert documents[0].path == (folder / "p2.txt")


def test_collect_from_yaml():
    yaml_path = Path(__file__).parent / "testfiles" / "data.yml"
    documents = get_files_from_yaml(
        yaml_source=yaml_path, file_cls=DocumentFile
    )
    assert len(documents) == 1
    assert str(documents[0].path) == str(
        Path(__file__).parent / "testfiles" / "test.md"
    )


def test_collect_from_yaml_source():
    yaml_path = Path(__file__).parent / "testfiles" / "data.yml"
    with open(yaml_path, encoding="utf-8") as file:
        yaml_source = yaml.safe_load(file)
    documents = get_files_from_yaml(
        yaml_source=yaml_source, file_cls=DocumentFile
    )
    assert len(documents) == 1
    assert str(documents[0].path) == str(
        Path(__file__).parent / "testfiles" / "test.md"
    )


def test_collect_from_yaml_source_error_mode():
    with raises(NonExistentModeInYamlSource):
        yaml_path = Path(__file__).parent / "testfiles" / "data.yml"
        _ = get_files_from_yaml(
            yaml_source=yaml_path, file_cls=DocumentFile, mode=DocumentFileMode.error,
        )
