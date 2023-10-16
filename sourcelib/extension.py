from dataclasses import dataclass
from typing import Callable, List, Optional


@dataclass(frozen=True)
class Extension:
    suffixes: tuple
    folder_coupled: Optional[Callable] = None


def get_extension_constant_mapping(globs):
    return create_extensions_mapping(get_extension_constants(globs))


def get_extension_constants(globs):
    return [
        value
        for key, value in globs.items()
        if isinstance(value, Extension) and key.isupper()
    ]


def create_extensions_mapping(extensions: List[Extension]):
    extensions_mapping = {}
    for extension in extensions:
        for suffix in extension.suffixes:
            if suffix in extensions_mapping:
                raise ValueError("Duplicate extension error")
            extensions_mapping[suffix] = extension
    return extensions_mapping
