from copy import deepcopy
from enum import Enum
from pathlib import Path
from typing import List, Mapping, Tuple, Union
import re
import yaml

from sourcelib.file import File, FileMode
from sourcelib.associations import Associations


class NoSourceFilesInFolderError(Exception):
    """Exception raised when no source files are found in a specified folder."""




class NonExistentModeInYamlSource(Exception):
    """Exception raised when a mode doesn't exist in the provided YAML source."""


def _get_yaml_data(source, mode):
    """
    Retrieve data from the source, either directly or from a YAML file.

    Args:
        source (Union[Mapping, str, Path]): The source, which can be a mapping, 
            a string indicating the path, or a Path object.
        mode (Enum): The mode to be used for extraction.

    Returns:
        dict: The extracted data.

    Raises:
        NonExistentModeInYamlSource: If the mode isn't present in the YAML data.
    """

    if isinstance(source, Mapping):
        data = deepcopy(source)
    if isinstance(source, (str, Path)):
        with open(source, encoding="utf-8") as file:
            data = yaml.safe_load(file)

    if mode.name not in data:
        raise NonExistentModeInYamlSource(
            f"mode '{mode.name}' not in data {data.keys()} in: {source}"
        )
    return data


def get_files_from_paths(
    file_cls: File,
    mode: Enum,
    paths: List[str],
    filters: List[str],
    excludes: List[str],
    regex=None,
    **kwargs,
):
    """
    Retrieve files from the provided paths based on specified criteria.

    Args:
        file_cls (File): The class for the files to be retrieved.
        mode (Enum): The mode associated with the file.
        paths (List[str]): The list of paths from which to retrieve files.
        filters (List[str]): A list of strings to filter the files.
        excludes (List[str]): A list of strings based on which files should be excluded.
        regex (str, optional): A regular expression to further filter files.

    Returns:
        List[File]: A list of files retrieved based on the criteria.
    """   

    files = []
    paths = set(paths)
    for path in paths:
        path = str(Path(path).expanduser())
        if any((exclude in path for exclude in excludes)):
            continue
        if filters and not any((filter in path for filter in filters)):
            continue
        if regex is not None and not re.search(regex, path):
            continue

        files.append(file_cls(mode=mode, path=path, **kwargs))
    return sorted(files, key=lambda k: k.path)


def get_files_from_path(
    file_cls: File, path: str, mode: Enum = FileMode.default, **kwargs
):
    """
    Retrieve files from a single path.

    Args:
        file_cls (File): The class for the files to be retrieved.
        path (str): The path from which to retrieve files.
        mode (Enum, optional): The mode associated with the file, default is FileMode.default.

    Returns:
        List[File]: A list of files retrieved from the path.
    """

    return get_files_from_paths(file_cls, mode, [path], [], [], None, **kwargs)


def get_files_from_folder(
    file_cls: File,
    folder: Union[str, Path],
    mode: Enum = FileMode.default,
    filters: List[str] = (),
    excludes: List[str] = (),
    regex=None,
    recursive=False,
    **kwargs,
):
    
    """
    Retrieve files from a specified folder based on criteria.

    Args:
        file_cls (File): The class for the files to be retrieved.
        folder (Union[str, Path]): The folder from which to retrieve files.
        mode (Enum, optional): The mode associated with the file, default is FileMode.default.
        filters (List[str], optional): List of strings to filter the files.
        excludes (List[str], optional): List of strings based on which files should be excluded.
        regex (str, optional): A regular expression to further filter files.
        recursive (bool, optional): Whether to search recursively in the folder.

    Returns:
        List[File]: A list of files retrieved from the folder based on the criteria.
    """

    all_sources = []
    folder = Path(folder)
    for extension in file_cls.EXTENSIONS:
        paths = (
            folder.rglob("*" + extension) if recursive else folder.glob("*" + extension)
        )
        sources = get_files_from_paths(
            file_cls, mode, paths, filters, excludes, regex, **kwargs
        )
        all_sources.extend(sources)

    if len(all_sources) == 0:
        raise NoSourceFilesInFolderError(file_cls, filters, excludes, regex, folder)
    return all_sources


# YAML_SOURCE_SCHEMA = {"mode": {'file_key': {'path': 'path_to_file', '**kwargs': '**kwargs'}}}


def get_files_from_yaml(
    yaml_source: Union[str, dict],
    file_cls: File,
    mode: Enum = FileMode.default,
    filters=(),
    excludes=(),
    regex=None,
    **kwargs,
):
    """
    Retrieve files specified in a YAML source.

    Args:
        yaml_source (Union[str, dict]): The YAML source, either as a path or a dictionary.
        file_cls (File): The class for the files to be retrieved.
        mode (Enum, optional): The mode associated with the file, default is FileMode.default.
        filters (Tuple[str], optional): Tuple of strings to filter the files.
        excludes (Tuple[str], optional): Tuple of strings based on which files should be excluded.
        regex (str, optional): A regular expression to further filter files.

    Returns:
        List[File]: A list of files retrieved based on the criteria specified in the YAML.
    """

    data = _get_yaml_data(yaml_source, mode)
    file_identifier = file_cls.IDENTIFIER

    paths = []
    for item in data[mode.name]:
        if file_identifier in item:
            paths.append(item[file_identifier].pop("path"))
            kwargs.update(item[file_identifier])

    return get_files_from_paths(
        file_cls, mode, paths, filters, excludes, regex, **kwargs
    )


def get_associations_from_yaml(
    yaml_source: Union[str, dict],
    file_classes: List[File],
    mode: Enum = FileMode.default,
):
    
    """
    Retrieve file associations specified in a YAML source.

    Args:
        yaml_source (Union[str, dict]): The YAML source, either as a path or a dictionary.
        file_classes (List[File]): The list of file classes to be retrieved.
        mode (Enum, optional): The mode associated with the file, default is FileMode.default.

    Returns:
        Associations: The associations of files retrieved based on the criteria specified in the YAML.
    """

    data = _get_yaml_data(yaml_source, mode)

    associations = Associations()
    for file_key, item in enumerate(data[mode.name]):
        file_key = str(file_key)
        associations.add_file_key(file_key=file_key, mode=mode)
        for _, file_data in file_classes.items():
            file_cls = file_data["class"]
            kwargs = file_data["kwargs"] if "kwargs" in file_data else {}
            file_identifier = file_cls.IDENTIFIER
            if file_identifier in item:
                path = item[file_identifier].pop("path")
                kwargs.update(item[file_identifier])
                file = file_cls(mode=mode, path=path, **kwargs)
                associations.add_file_with_key(file_key=file_key, file=file)
    return associations


def copy_from_yml(
    yaml_source: Union[Path, dict],
    file_cls: File,
    copy_path: Path,
    modes: Tuple[Enum] = (FileMode.default,),
    **kwargs,
):
    """
    Copy files specified in a YAML source to a destination path.

    Args:
        yaml_source (Union[Path, dict]): The YAML source, either as a path or a dictionary.
        file_cls (File): The class for the files to be copied.
        copy_path (Path): The destination path where files should be copied.
        modes (Tuple[Enum], optional): The modes associated with the files, default is (FileMode.default,).
    """
    
    data = []
    for mode in modes:
        data.extend(
            get_files_from_yaml(
                yaml_source=yaml_source,
                file_cls=file_cls,
                mode=mode,
                **kwargs,
            )
        )
    for d in data:
        d.copy(copy_path)
