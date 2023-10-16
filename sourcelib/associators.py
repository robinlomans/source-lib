from sourcelib.file import File


def stem_file_associater(file: File) -> str:
    """To group files by their names without considering extensions, use this associator. Give it a file, and it provides the stem (the filename without its extension).

    Args:
        file (File): The file whose stem is to be extracted.

    Returns:
        str: The stem of the file.

    Examples:
        >>> file = File("/path/to/image.jpg")
        >>> stem_file_associater(file)
        'image'
    """
    return file.path.stem


class AnyOneAssociater:
    """Returns the class name as the association name when called.

    Examples:
        >>> associater = AnyOneAssociater()
        >>> associater(file)
        'AnyOneAssociater'
    """

    def __call__(self, file: File) -> str:
        return self.__class__.__name__


class StemSplitterAssociater:
    """To group files using a segment of their name, such as matching between data_2023.txt and overview_2023.pdf, use StemSplitterAssociater. It allows you to pick delimiter symbols (like _) to segment the filename for categorization e.g., in this case the year 2023.

    Args:
        split_symbols (tuple): Tuple of symbols used to split the file stem.

    Examples:
        >>> associater = StemSplitterAssociater(split_symbols=("_", "-"))
        >>> file = File("/path/to/image_01-version.jpg")
        >>> associater(file)
        'image'
    """

    def __init__(self, split_symbols: tuple):
        self._split_symbols = split_symbols
        super().__init__()

    def __call__(self, file: File) -> str:
        association_name = file.path.stem
        for split_symbol in self._split_symbols:
            association_name = association_name.split(split_symbol)[0]
        return association_name
