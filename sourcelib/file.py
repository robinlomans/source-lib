from abc import abstractmethod
from copy import copy
from pathlib import Path
from typing import Any, Union

from creationism.registration.factory import RegistrantFactory

from sourcelib.copy import copy as copy_source
from sourcelib.extension import Extension
from sourcelib.mode import DefaultMode, Mode


class File(RegistrantFactory):

    REPLACE = False
    RECURSIVE = True

    EXTENSIONS = Extension
    MODES = Mode

    def __init__(
        self,
        path: Union[str, Path],
        mode: Union[str, Mode] = DefaultMode,
    ):
        self.mode = self.__class__.MODES.create(mode)
        self.path = Path(path)
        self.extension: Extension = self.__class__.EXTENSIONS.create(self.path.suffix)
        self.original_path = copy(path)

    @abstractmethod
    def open(self) -> Any:
        """method to open file

        Returns:
            Any: content of opened file
        """

    @property
    def exists(self) -> bool:
        return self.path.exists()

    def copy(self, destination_folder: Path) -> None:
        if self.extension.FOLDER_COUPLED:
            copy_source(self.path.with_suffix(""), destination_folder)
        self.path = copy_source(self.path, destination_folder)

    def __str__(self) -> str:
        return f"Mode: {str(self.mode.name)} | Path:  {str(self.path)}"
