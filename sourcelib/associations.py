import itertools
import warnings
from abc import abstractmethod
from collections import UserDict
from pathlib import Path
from typing import Callable, List, Optional

from sourcelib.file import File


def stem_file_associater(file: File):
    return file.path.stem


class Associator:
    def __init__(self):
        """_summary_"""

    @abstractmethod
    def __call__(self, file: File):
        """_summary_

        Args:
            file (File): _description_

        Returns:
            _type_: _description_
        """


class AnyOneAssociater(Associator):
    def __call__(self, file: File):
        return self.__class__.__name__


class StemSplitterAssociater(Associator):
    def __init__(self, split_symbols: tuple):
        self._split_symbols = split_symbols
        super().__init__()

    def __call__(self, file: File):
        association_name = file.path.stem
        for split_symbol in self._split_symbols:
            association_name = association_name.split(split_symbol)[0]
        return association_name


class AssociatedFiles(UserDict):
    def __init__(self, file_key):
        self._file_key = file_key
        super().__init__({})

    def add_file(self, file):
        self.setdefault(type(file), []).append(file)


class Associations(UserDict):
    def __init__(self):
        super().__init__({})

    def add_file_key(self, file_key: str):
        self.setdefault(file_key, AssociatedFiles(file_key))

    def add_file(self, file: Path, associater: Callable, exact_match, required):
        file_key = self._associate(file, associater, exact_match)
        if file_key is None and not required:
            return
        self[file_key].add_file(file)

    def _associate(self, file: Path, associater: Callable, exact_match: bool) -> str:
        file_association_key = associater(file)

        for file_key in self:
            if exact_match:
                if file_key == file_association_key:
                    return file_key
            elif file_key in file_association_key:
                return file_key

    @property
    def associated_files(self):
        return [
            tuple(itertools.chain.from_iterable(values.values()))
            for values in self.values()
        ]


def associate_files(
    files1: List,
    files2: List,
    associations: Optional[Associations] = None,
    associator: Callable = stem_file_associater,
    exact_match=False,
) -> Associations:

    if associations is None:
        associations = Associations()

    for file1 in files1:

        file_key = associator(file1)
        associations.add_file_key(file_key=file_key)
        associations.add_file(
            file=file1, associater=associator, exact_match=exact_match, required=True
        )

    for file2 in files2:
        associations.add_file(
            file=file2, associater=associator, exact_match=exact_match, required=False
        )

    # remove unpaired
    remove_keys = []
    for file_key, files in associations.items():
        # check if only 1 file type and check if only one item of that file type
        if len(list(files.keys())) <= 1 and len(list(dict(files).values())[0]) <= 1:
            remove_keys.append(file_key)

    for remove_key in remove_keys:
        warnings.warn(f"Could not find matching files for key: {remove_key}")
        del associations[remove_key]

    return associations
