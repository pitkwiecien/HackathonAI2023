from typing import List

from objects.indexed_object import IndexedObject
from openai_asker import OpenaiAsker
from descripted_file import DescriptedFile


class FileDescriptor:
    def __init__(self, docs: List[IndexedObject]):
        self.docs = docs

    def describe(self):
        return tuple(map(lambda x: DescriptedFile(x.metadata["path"], OpenaiAsker.describe_file(x)), self.docs))
