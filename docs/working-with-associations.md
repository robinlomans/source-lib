---
title: Working with Associations
---

# Working with Associations

## Associators

Central to this module is the concept of Associators, which are functions or objects that take in a file path and return a key which represents a category or group that the file belongs to.

**stem_file_associater**.  To group files by their names without considering extensions, use this associator. Give it a file, and it provides the stem (the filename without its extension).

**StemSplitterAssociater**. To group files using a segment of their name, such as matching between data_2023.txt and overview_2023.pdf, use StemSplitterAssociater. It allows you to pick delimiter symbols (like _) to segment the filename for categorization e.g., in this case the year 2023.

## The Associations Class

Now that we have a way to generate keys for files, it's time to put them together. The `Associations` class is a container that allows you to group files under their respective keys.

### Groupings with AssociatedFiles

With a method in place for creating file keys, we introduce the Associations class. It organizes files under their corresponding keys.

## associate_files

To associate files seamlessly, employ the associate_files function. Provide two lists of files, and it'll establish links based on the associator you select. It guarantees files from the first list have matches and alerts you if any are unpaired from the second list.


