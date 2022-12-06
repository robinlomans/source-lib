# sourcelib

[![PyPI version](https://badge.fury.io/py/sourcelib.svg)](https://badge.fury.io/py/sourcelib)
[![tests](https://github.com/martvanrijthoven/source-lib/actions/workflows/tests.yml/badge.svg)](https://github.com/martvanrijthoven/source-lib/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/martvanrijthoven/source-lib/branch/main/graph/badge.svg?token=HTW167NRS2)](https://codecov.io/gh/martvanrijthoven/source-lib)
[![codeinspector](https://api.codiga.io/project/34464/score/svg)](https://app.codiga.io/public/project/34464/source-lib/dashboard)


Source lib offers the possibility to collect files from different types and associate them. 
For example imagenet images and annotations.



```python
data_files = get_files_from_folder(file_cls=SuperHeroDataFile, folder='./', mode=SuperHeroMode.default)
image_files = get_files_from_folder(file_cls=SuperHeroImageFile, folder='./', mode=SuperHeroMode.default)
associations = associate_files(image_files, data_files)
```