from typing import List

from objects.indexed_object import IndexedObject
from openai_asker import OpenaiAsker


class FileDescriptor:
    def __init__(self, docs: List[IndexedObject]):
        self.docs = docs
        self.asker = OpenaiAsker()

    def describe(self):
        return tuple(map(lambda x: self.describe_file(x), self.docs))

    @staticmethod
    def describe_file(obj: IndexedObject):

        ai_result = None
        return IndexedObject(ai_result, code=obj.data, **obj.metadata)
