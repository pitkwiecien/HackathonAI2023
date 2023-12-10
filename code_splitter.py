from objects.indexed_object import IndexedObject
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import LanguageParser
from langchain.text_splitter import RecursiveCharacterTextSplitter


class CodeSplitter:
    """
    A class to split code documents into smaller chunks and convert them into IndexedObject instances.

    Attributes:
    - loader: GenericLoader instance for loading code documents.
    - docs: List of documents loaded by the loader and split into smaller chunks.
    """

    def __init__(self, path):
        """
        Initializes the CodeSplitter with a path to load code documents.

        Args:
        - path (str): The filesystem path containing code documents.
        """
        self.loader = GenericLoader.from_filesystem(
            path=path,
            glob='**/*',
            suffixes=[".py", ".js", ".html"],
            parser=LanguageParser()
        )
        self.docs = self.loader.load()
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=50
        )
        self.docs = splitter.split_documents(documents=self.docs)

    def to_indexed_objects(self):
        """
        Converts the split code documents into IndexedObject instances.

        Returns:
        - List[IndexedObject]: List of IndexedObject instances created from the split code documents.
        """
        return [IndexedObject.create_object(doc.page_content, path=doc.metadata['source']) for doc in self.docs]

    @staticmethod
    def print_indexed_objects(indexed_objects):
        """
        Prints the details of IndexedObject instances.

        Args:
        - indexed_objects (List[IndexedObject]): List of IndexedObject instances to print.
        """
        for obj in indexed_objects:
            print(obj)
