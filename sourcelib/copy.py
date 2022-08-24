import os
from dataclasses import dataclass
from pathlib import Path
from shutil import copy2, copytree




@dataclass(frozen=True)
class NonExistingSourceFileError(Exception):
    source_path: Path
    destination_folder: Path

    def __post_init__(self):
        super().__init__(self._message())

    def _message(self):
        return f"Can not copy {self.source_path} because it does not exists"


def copy(source_path: Path, destination_folder: Path) -> Path:

    if not source_path.exists():
        raise NonExistingSourceFileError(source_path, destination_folder)

    destination_path = _initialize_destination_path(source_path, destination_folder)

    if not destination_path.exists():
        _transfer(source_path, destination_path)
        print(f"| Copied '{source_path}' | To: '{destination_path}'\n.")
    return destination_path


def _initialize_destination_path(source: Path, destination_folder: Path) -> Path:
    destination_folder = Path(destination_folder).resolve()
    destination_folder.mkdir(parents=True, exist_ok=True)
    return destination_folder / source.name


def _transfer(source: Path, destination_path: Path) -> None:
    transfer_function = copytree if os.path.isdir(source) else copy2
    transfer_function(str(source), str(destination_path))



