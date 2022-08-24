from pathlib import Path
from sourcelib.copy import NonExistingSourceFileError
from sourcelib.collect import copy_from_yml
from sourcelib.file import File
from tests.testfiles.testclasses import DocumentCollector, DocumentFile, TptFileReader
from pytest import raises


def test_file(tmp_path):
    markdown_path = tmp_path / 'testfiles' / 'test.md'
    document_file = File.get_registrant('doc')
    markdown_file = document_file(path=markdown_path)
    print(markdown_file)
    assert isinstance(markdown_file, DocumentFile)


def test_open_file():
    markdown_path = Path(__file__).parent / 'testfiles' / 'test.md'
    document_file = File.get_registrant('doc')
    markdown_file = document_file(path=markdown_path)
    content = markdown_file.open()
    assert content == "hello from markdown"


def test_copy_file(tmp_path):
    markdown_path = Path(__file__).parent / 'testfiles' /'test.md'
    document_file = File.get_registrant('doc')
    markdown_file: DocumentFile = document_file(path=markdown_path)
    assert markdown_file.exists
    markdown_file.copy(tmp_path)
    output_path = (tmp_path / 'test.md')
    assert output_path.exists()
    assert markdown_file.path == output_path
    assert markdown_file.original_path == markdown_path
    assert markdown_file.exists



def test_copy_file_with_coupled_folder(tmp_path):
    tpt_path = Path(__file__).parent / 'testfiles' /'testparts.tpt'
    document_file = File.get_registrant('doc')
    tpt_file: DocumentFile = document_file(path=tpt_path, file_reader=TptFileReader())
    assert tpt_file.exists
    tpt_file.copy(tmp_path)
    output_path = (tmp_path / 'testparts.tpt')
    assert output_path.exists()
    assert (tmp_path / tpt_path.with_suffix('')).is_dir()
    content = tpt_file.open()
    assert content == "part1part2"


def test_copy_error(tmp_path):
    with raises(NonExistingSourceFileError) as errors:
        path = Path(__file__).parent / 'testfiles' / 'notexisting.txt'
        document_file = File.get_registrant('doc')
        txt_file: DocumentFile = document_file(path=path, file_reader=TptFileReader())
        txt_file.copy(tmp_path)


def test_copy_from_yaml(tmp_path: Path):
    yaml_path = Path(__file__).parent / "testfiles" / "data.yml"
    copy_from_yml(yaml_path, tmp_path, DocumentCollector,  modes=('default',), file_types=('doc', ))
    assert (tmp_path/ 'test.md').exists()
