import warnings
from collections import UserDict
from pathlib import Path
from typing import Callable, List, Optional

from sourcelib.file import File, ModeMisMatchError


class AssociatedFiles(UserDict):
    """Represents files associated with a key and mode.

    Args:
        file_key (str): The key associated with the files.
        mode (str): The mode of the associated files.

    Examples:
        >>> associated_files = AssociatedFiles(file_key="key1", mode="mode1")
        >>> associated_files.add_file(file)
    """
    def __init__(self, file_key, mode):
        self._file_key = file_key
        self._mode = mode
        super().__init__({})

    def add_file(self, file: File):
        if file.mode != self._mode:
            raise ModeMisMatchError("Mode does not match")

        if type(file) not in self or file not in self[type(file)]:
            self.setdefault(file.IDENTIFIER, []).append(file)

class Associations(UserDict):
    """Represents a collection of associated files.

    Examples:
        >>> associations = Associations()
        >>> associations.add_file_key(file_key="key1", mode="mode1")
    """
    def __init__(self):
        super().__init__({})

    def add_file_key(self, file_key: str, mode):
        self.setdefault(file_key, AssociatedFiles(file_key, mode))

    def add_file_with_key(self, file_key, file):
        self[file_key].add_file(file)

    def add_file(self, file: Path, associater: Callable, exact_match: bool, required: bool):
        file_key = self._associate(file, associater, exact_match)
        if file_key is None and not required:
            return
        self[file_key].add_file(file)

    def _associate(self, file: Path, associater: Callable, exact_match: bool) -> Optional[str]:
        file_association_key = associater(file)

        for file_key in self:
            if exact_match:
                if file_key == file_association_key:
                    return file_key
            elif file_key in file_association_key:
                return file_key
        return None

def associate_files(files1: List[File], files2: List[File], associations: Optional[Associations] = None, 
                    associator: Callable = stem_file_associater, exact_match=False) -> Associations:
    """Associates two lists of files based on an associator.

    Args:
        files1 (List[File]): The first list of files to be associated.
        files2 (List[File]): The second list of files to be associated.
        associations (Optional[Associations]): Pre-existing associations. Defaults to None.
        associator (Callable): The function used to determine associations. Defaults to stem_file_associater.
        exact_match (bool): Flag to determine if exact matches are required. Defaults to False.

    Returns:
        Associations: The associations formed from the provided files.

    Examples:
        >>> files1 = [File("/path/to/image1.jpg"), File("/path/to/image2.jpg")]
        >>> files2 = [File("/path/to/image1_copy.jpg"), File("/path/to/image3.jpg")]
        >>> result = associate_files(files1, files2)
    """

    if associations is None:
        associations = Associations()

    for file1 in files1:
        file_key = associator(file1)
        associations.add_file_key(file_key=file_key, mode=file1.mode)
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
        if len(list(files.keys())) <= 1 and len(list(dict(files).values())[0]) <= 1:
            remove_keys.append(file_key)

    for remove_key in remove_keys:
        warnings.warn(f"Could not find matching files for key: {remove_key}")
        del associations[remove_key]

    return associations
