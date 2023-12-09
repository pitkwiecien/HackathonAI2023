from typing import List

from objects.indexed_object import IndexedObject
from openai_asker import OpenaiAsker


class FileDescriptor:
    def __init__(self, docs: List[IndexedObject]):
        self.docs = docs

    def describe(self):
        return tuple(map(lambda x: self.describe_file(x), self.docs))

    @staticmethod
    def describe_file(obj: IndexedObject):
        asker = OpenaiAsker.describe_file("")
        return IndexedObject(ai_result, code=obj.data, **obj.metadata)
