from tests.testfiles.testclasses import DocumentExtension, MarkDownExtension, TextExtension

def test_extension():
    txt_extension = DocumentExtension.create(".txt")
    assert isinstance(txt_extension, TextExtension)
    assert not isinstance(txt_extension, MarkDownExtension)
    assert txt_extension is DocumentExtension.create('.txt')
    assert txt_extension is not DocumentExtension.create('.md')

    md_extension = DocumentExtension.create(".md")
    assert isinstance(md_extension, MarkDownExtension)
    assert not isinstance(md_extension, TextExtension)
    assert md_extension is DocumentExtension.create('.md')
    assert md_extension is not DocumentExtension.create('.txt')
  
  