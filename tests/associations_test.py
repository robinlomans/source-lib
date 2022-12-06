from pathlib import Path

from pytest import raises, warns
from sourcelib.associations import (AnyOneAssociater, StemSplitterAssociater,
                                    associate_files, stem_file_associater)
from sourcelib.collect import get_files_from_folder
from sourcelib.file import ModeMisMatchError

from .testfiles.testclasses import DocumentFile, DocumentFileMode


def test_stem_file_associater():
    folder = Path(__file__).parent / "testfiles" / "testparts"
    txt_files = get_files_from_folder(
        file_cls=DocumentFile, folder=folder, filters="txt"
    )
    md_files = get_files_from_folder(file_cls=DocumentFile, folder=folder, filters="md")
    associations = associate_files(
        files1=txt_files, files2=md_files, associator=stem_file_associater
    )
    assert len(associations) == 2
    for _, items in associations.items():
        assert len(items[DocumentFile.IDENTIFIER]) == 2


def test_stem_file_associater_property():
    folder = Path(__file__).parent / "testfiles" / "testparts"
    txt_files = get_files_from_folder(
        file_cls=DocumentFile, folder=folder, filters="txt"
    )
    md_files = get_files_from_folder(file_cls=DocumentFile, folder=folder, filters="md")
    associations = associate_files(
        files1=txt_files, files2=md_files, associator=stem_file_associater
    )
    for item in associations:
        assert len(item) == 2


def test_stem_file_associater_exact():
    folder = Path(__file__).parent / "testfiles" / "testparts"
    txt_files = get_files_from_folder(
        file_cls=DocumentFile, folder=folder, filters="txt"
    )
    md_files = get_files_from_folder(
        file_cls=DocumentFile, folder=folder / "md", filters="md"
    )
    associations = associate_files(
        files1=txt_files,
        files2=md_files,
        associator=stem_file_associater,
        exact_match=True,
    )
    assert len(associations) == 2
    for _, items in associations.items():
        assert len(items[DocumentFile.IDENTIFIER]) == 2


def test_stem_split_file_associater():
    folder = Path(__file__).parent / "testfiles" / "testparts"
    txt_files = get_files_from_folder(
        file_cls=DocumentFile, folder=folder, filters="txt"
    )
    md_files = get_files_from_folder(file_cls=DocumentFile, folder=folder, filters="md")
    associations = associate_files(
        files1=txt_files, files2=md_files, associator=StemSplitterAssociater(",")
    )
    assert len(associations) == 2
    for _, items in associations.items():
        assert len(items[DocumentFile.IDENTIFIER]) == 2


def test_stem_file_associater_remove_unpaired():
    with warns(UserWarning):
        folder = Path(__file__).parent / "testfiles" / "testparts"
        txt_files = get_files_from_folder(
            file_cls=DocumentFile, folder=folder, filters="txt"
        )
        md_files = get_files_from_folder(
            file_cls=DocumentFile,
            folder=folder,
            filters="md",
            excludes=("p2",),
        )

        associations = associate_files(
            files1=txt_files, files2=md_files, associator=stem_file_associater
        )
        assert len(associations) == 1


def test_stem_file_associater_anyone_associater():
    folder = Path(__file__).parent / "testfiles" / "testparts"
    txt_files = get_files_from_folder(
        file_cls=DocumentFile, folder=folder, filters="txt"
    )
    md_files = get_files_from_folder(file_cls=DocumentFile, folder=folder, filters="md")

    associations = associate_files(
        files1=txt_files, files2=md_files, associator=AnyOneAssociater()
    )
    assert len(associations) == 1
    for _, items in associations.items():
        assert len(items[DocumentFile.IDENTIFIER]) == 4


def test_mode_mismatch_error():
    with raises(ModeMisMatchError):
        folder = Path(__file__).parent / "testfiles" / "testparts"
        txt_files = get_files_from_folder(
            file_cls=DocumentFile,
            folder=folder,
            filters="txt",
            mode=DocumentFileMode.default,
        )
        md_files = get_files_from_folder(
            file_cls=DocumentFile,
            folder=folder,
            filters="md",
            mode=DocumentFileMode.error,
        )

        associate_files(
            files1=txt_files, files2=md_files, associator=AnyOneAssociater()
        )
