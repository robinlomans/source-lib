from pathlib import Path
from typing import List, Union

import yaml

from sourcelib.file import File
from sourcelib.mode import Mode


class NoSourceFilesInFolderError(Exception):
    """_summary_

    Args:
        Exception (_type_): _description_

    Raises:
        NoSourceFilesInFolderError: _description_
        NonExistentModeInYamlSource: _description_

    Returns:
        _type_: _description_
    """


class NonExistentModeInYamlSource(Exception):
    """_summary_

    Args:
        Exception (_type_): _description_

    Raises:
        NoSourceFilesInFolderError: _description_
        NonExistentModeInYamlSource: _description_

    Returns:
        _type_: _description_
    """


class FileCollector:
    FILE_CLASS = File

    @classmethod
    def get_files_from_path(cls, file_type, mode: str, path: str, **kwargs):
        class_type = cls.FILE_CLASS.get_registrant(file_type)
        return sorted(get_files_from_path(
            class_type=class_type, mode=mode, path=path, **kwargs
        ), key=lambda k: k.path)

    @classmethod
    def get_files_from_folder(
        cls,
        file_type,
        folder: Union[str, Path],
        mode: str = "default",
        filters: List[str] = (),
        excludes: List[str] = (),
        recursive=False,
        **kwargs,
    ):
        class_type = cls.FILE_CLASS.get_registrant(file_type)
        return sorted(get_files_from_folder(
            class_type=class_type,
            folder=folder,
            mode=mode,
            filters=filters,
            excludes=excludes,
            recursive=recursive,
            **kwargs,
        ), key=lambda k: k.path)

    @classmethod
    def get_files_from_yaml(
        cls,
        file_type,
        yaml_source: Union[str, dict],
        mode: str = "default",
        filters=[],
        excludes=[],
        **kwargs,
    ):
        class_type = cls.FILE_CLASS.get_registrant(file_type)
        return sorted(get_files_from_yaml(
            class_type=class_type,
            file_indentifier=file_type,
            yaml_source=yaml_source,
            mode=mode,
            filters=filters,
            excludes=excludes,
            **kwargs,
        ), key=lambda k: k.path)


def get_files_from_paths(
    cls: Union[str, type],
    mode: Union[str, Mode],
    paths: List[str],
    filters: List[str],
    excludes: List[str],
    **kwargs,
):
    files = []
    paths = set(paths)
    for path in paths:
        path = str(Path(path).expanduser())
        if any([exclude in path for exclude in excludes]):
            continue
        if filters and not any([filter in path for filter in filters]):
            continue
        files.append(cls(mode=mode, path=path, **kwargs))
    return files


def get_files_from_path(class_type: type, mode: str, path: str, **kwargs):
    return get_files_from_paths(class_type, mode, [path], [], [], **kwargs)


def get_files_from_folder(
    class_type: type,
    folder: Union[str, Path],
    mode: str = "default",
    filters: List[str] = (),
    excludes: List[str] = (),
    recursive=False,
    **kwargs,
):

    all_sources = []
    folder = Path(folder)
    for extension in class_type.EXTENSIONS.names():
        paths = (
            folder.rglob("*" + extension) if recursive else folder.glob("*" + extension)
        )
        sources = get_files_from_paths(
            class_type, mode, paths, filters, excludes, **kwargs
        )
        all_sources.extend(sources)

    if all_sources == []:
        raise NoSourceFilesInFolderError(class_type, filters, excludes, folder)
    return all_sources


# YAML_SOURCE_SCHEMA = {"mode": {'file_key': {'path': 'path_to_file', '**kwargs': '**kwargs'}}}


def get_files_from_yaml(
    class_type: type,
    file_indentifier: str,
    yaml_source: Union[str, dict],
    mode: str = "default",
    filters=[],
    excludes=[],
    **kwargs,
):

    data = {}

    if isinstance(yaml_source, dict):
        data = yaml_source
    elif isinstance(yaml_source, str) or isinstance(yaml_source, Path):
        with open(yaml_source) as file:
            data = yaml.load(file, Loader=yaml.FullLoader)

    paths = []
    if mode not in data:
        raise NonExistentModeInYamlSource(
            f"mode '{mode}' not in data {data.keys()} in: {yaml_source}"
        )

    for item in data[mode]:
        if file_indentifier in item:
            paths.append(item[file_indentifier].pop("path"))
            kwargs.update(item[file_indentifier])

    return get_files_from_paths(class_type, mode, paths, filters, excludes, **kwargs)


def copy_from_yml(
    data_config, copy_path, file_collector: FileCollector, modes=(), file_types=()
):
    data = []
    for mode in modes:
        for file_type in file_types:
            clss_type = file_collector.FILE_CLASS.get_registrant(file_type)
            data.extend(
                get_files_from_yaml(clss_type, file_type, data_config, mode=mode)
            )
    for d in data:
        d.copy(copy_path)
