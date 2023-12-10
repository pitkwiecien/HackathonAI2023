from typing import List
from objects.indexed_object import IndexedObject
from openai_asker import OpenaiAsker
from descripted_file import DescriptedFile

class FileDescriptor:
    """
    A class to describe files using IndexedObject instances.

    Attributes:
    - docs (List[IndexedObject]): List of IndexedObject instances representing files.
    """

    def __init__(self, docs: List[IndexedObject]):
        """
        Initializes the FileDescriptor with a list of IndexedObject instances.

        Args:
        - docs (List[IndexedObject]): List of IndexedObject instances representing files.
        """
        self.docs = docs

    def describe(self):
        """
        Describes files using OpenaiAsker and creates DescriptedFile instances.

        Returns:
        - tuple: Tuple containing DescriptedFile instances for the described files.
        """
        return tuple(map(lambda x: DescriptedFile(x.metadata["path"], OpenaiAsker.describe_file(x)), self.docs))
