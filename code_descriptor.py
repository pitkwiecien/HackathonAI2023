from typing import List

from descripted_file import DescriptedFile
from objects.indexed_object import IndexedObject
from openai_asker import OpenaiAsker


class CodeDescriptor:
    def __init__(self, docs: List[IndexedObject], files: List[DescriptedFile]):
        self.docs = docs
        self.files = files

    def describe(self):
        for doc in self.docs:
            matching_field = None
            print(doc.metadata["path"])
            for f in self.files:
                print(f.path)
                if f.path == doc.metadata["path"]:
                    matching_field = f
            doc.metadata["meaning"] = matching_field.file_desc
            result = OpenaiAsker.describe_code(doc)
            if matching_field:
                matching_field.a.append(result)

