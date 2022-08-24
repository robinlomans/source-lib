from pathlib import Path

from pytest import warns
from sourcelib.associations import (
    AnyOneAssociater,
    StemSplitterAssociater,
    associate_files,
    stem_file_associater,
)

from .testfiles.testclasses import DocumentCollector, DocumentFile


def test_stem_file_associater():
    folder = Path(__file__).parent / "testfiles" / "testparts"
    txt_files = DocumentCollector.get_files_from_folder(
        "doc", folder=folder, filters="txt"
    )
    md_files = DocumentCollector.get_files_from_folder(
        "doc", folder=folder / "md", filters="md"
    )
    associations = associate_files(
        files1=txt_files, files2=md_files, associator=stem_file_associater
    )
    assert len(associations) == 2
    for _, items in associations.items():
        assert len(items[DocumentFile]) == 2


def test_stem_file_associater_property():
    folder = Path(__file__).parent / "testfiles" / "testparts"
    txt_files = DocumentCollector.get_files_from_folder(
        "doc", folder=folder, filters="txt"
    )
    md_files = DocumentCollector.get_files_from_folder(
        "doc", folder=folder / "md", filters="md"
    )
    associations = associate_files(
        files1=txt_files, files2=md_files, associator=stem_file_associater
    )
    for item in associations.associated_files:
        assert len(item) == 2


def test_stem_file_associater_exact():
    folder = Path(__file__).parent / "testfiles" / "testparts"
    txt_files = DocumentCollector.get_files_from_folder(
        "doc", folder=folder, filters="txt"
    )
    md_files = DocumentCollector.get_files_from_folder(
        "doc", folder=folder / "md", filters="md"
    )
    associations = associate_files(
        files1=txt_files,
        files2=md_files,
        associator=stem_file_associater,
        exact_match=True,
    )
    assert len(associations) == 2
    for _, items in associations.items():
        assert len(items[DocumentFile]) == 2


def test_stem_split_file_associater():
    folder = Path(__file__).parent / "testfiles" / "testparts"
    txt_files = DocumentCollector.get_files_from_folder(
        "doc", folder=folder, filters="txt"
    )
    md_files = DocumentCollector.get_files_from_folder(
        "doc", folder=folder / "md", filters="md"
    )
    associations = associate_files(
        files1=txt_files, files2=md_files, associator=StemSplitterAssociater(",")
    )
    assert len(associations) == 2
    for _, items in associations.items():
        assert len(items[DocumentFile]) == 2


def test_stem_file_associater_remove_unpaired():
    with warns(UserWarning):
        folder = Path(__file__).parent / "testfiles" / "testparts"
        txt_files = DocumentCollector.get_files_from_folder(
            "doc", folder=folder, filters=("txt",)
        )
        md_files = DocumentCollector.get_files_from_folder(
            "doc", folder=folder / "md", filters=("md",), excludes=("p2",)
        )
        associations = associate_files(
            files1=txt_files, files2=md_files, associator=stem_file_associater
        )
        assert len(associations) == 1


def test_stem_file_associater_anyone_associater():
    folder = Path(__file__).parent / "testfiles" / "testparts"
    txt_files = DocumentCollector.get_files_from_folder(
        "doc", folder=folder, filters=("txt",)
    )
    md_files = DocumentCollector.get_files_from_folder(
        "doc", folder=folder / "md", filters=("md",)
    )

    associations = associate_files(
        files1=txt_files, files2=md_files, associator=AnyOneAssociater()
    )
    assert len(associations) == 1
    for _, items in associations.items():
        assert len(items[DocumentFile]) == 5
