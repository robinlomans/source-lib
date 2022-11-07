from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Extension:
    suffixes: tuple
    folder_coupled: bool = False


def create_extensions_mapping(extensions: List[Extension]):
    extensions_mapping = {}
    for extension in extensions:
        for suffix in extension.suffixes:
            if suffix in extensions_mapping:
                raise ValueError("duplicate extension error")
            extensions_mapping[suffix] = extension
    return extensions_mapping
