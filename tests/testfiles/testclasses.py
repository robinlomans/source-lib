from pathlib import Path
from sourcelib.collect import FileCollector
from sourcelib.extension import Extension
from sourcelib.file import File
from sourcelib.mode import Mode


class DocumentExtension(Extension):
    ...

@DocumentExtension.register((".txt",))
class TextExtension(DocumentExtension):
    ...


@DocumentExtension.register((".md",))
class MarkDownExtension(DocumentExtension):
    ...


@DocumentExtension.register((".tpt",))
class TextPartsExtension(DocumentExtension):
    FOLDER_COUPLED = True


class FileReader:
    ...


class StandardFileReader(FileReader):
    def __call__(self, path):
        with open(path, encoding="utf-8") as file:
            return file.read()


class TptFileReader(FileReader):
    """reads txt files in folder with same name of a .tpt file and concatenates content"""

    def __call__(self, path: Path):
        paths = sorted(list(path.with_suffix("").glob("*.txt")))
        content = str()
        for p in paths:
            with open(p, encoding="utf-8") as file:
                content += file.read()
        return content


@File.register(("doc",))
class DocumentFile(File):

    EXTENSIONS = DocumentExtension

    def __init__(
        self, path, mode=Mode.create("default"), file_reader=StandardFileReader()
    ):
        super().__init__(path=path, mode=mode)
        self.file_reader = file_reader

    def open(self):
        return self.file_reader(self.path)

class DocumentCollector(FileCollector):
    
    FILE_CLASS = File
