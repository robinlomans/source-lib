from sourcelib.extension import Extension, create_extensions_mapping
from pathlib import Path

from pytest import raises
from sourcelib.collect import copy_from_yml
from sourcelib.copy import NonExistingSourceFileError
from tests.testfiles.testclasses import DocumentFile
from sourcelib.file import FileMode


def test_open_file():
    markdown_path = Path(__file__).parent / "testfiles" / "test.md"
    DocumentFile(path=markdown_path)


def test_copy_file(tmp_path: Path):
    markdown_path = Path(__file__).parent / "testfiles" / "test.md"
    markdown_file = DocumentFile(path=markdown_path)
    assert markdown_file.exists
    markdown_file.copy(tmp_path)
    output_path = tmp_path / "test.md"
    assert output_path.exists()
    assert markdown_file.path == output_path
    assert markdown_file.original_path != markdown_path
    print(markdown_file)


def test_copy_file_with_coupled_folder(tmp_path: Path):
    tpt_path = Path(__file__).parent / "testfiles" / "testparts.tpt"
    tpt_file: DocumentFile = DocumentFile(path=tpt_path)
    assert tpt_file.exists
    tpt_file.copy(tmp_path)
    output_path = tmp_path / "testparts.tpt"
    assert output_path.exists()
    assert (tmp_path / tpt_path.with_suffix("")).is_dir()


def test_copy_error(tmp_path: Path):
    with raises(NonExistingSourceFileError):
        path = Path(__file__).parent / "testfiles" / "notexisting.txt"
        txt_file = DocumentFile(path=path)
        txt_file.copy(tmp_path)


def test_copy_from_yaml(tmp_path: Path):
    yaml_path = Path(__file__).parent / "testfiles" / "data.yml"
    copy_from_yml(
        yaml_path,
        copy_path=tmp_path,
        file_cls=DocumentFile,
        modes=(FileMode.default,),
    )
    assert (tmp_path / "test.md").exists()


def test_duplace_extension():
    with raises(ValueError):
        extension_txt = Extension(".txt")
        create_extensions_mapping([extension_txt, extension_txt])