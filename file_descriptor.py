from typing import List

from objects.indexed_object import IndexedObject
from openai_asker import OpenaiAsker


class FileDescriptor:
    def __init__(self, docs: List[IndexedObject]):
        self.docs = docs

    def describe(self):
        return tuple(map(lambda x: OpenaiAsker.describe_file(x), self.docs))
