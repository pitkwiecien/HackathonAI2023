from objects.indexed_object import IndexedObject

from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser
from langchain.text_splitter import Language


class CodeSplitter:
    def __init__(self, path):
        self.loader = GenericLoader.from_filesystem(
            path=path,
            glob='*',
            suffixes=[".py"],
            parser=LanguageParser(language=Language.PYTHON)
        )
        self.docs = self.loader.load()

    def to_indexed_objects(self):
        # print(self.docs[0].page_content)
        return [IndexedObject.create_object(doc.page_content, path=doc.metadata['source']) for doc in self.docs]

    @staticmethod
    def print_indexed_objects(indexed_objects):
        for obj in indexed_objects:
            print(obj)
