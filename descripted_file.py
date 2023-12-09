from typing import List


class DescriptedFile:
    def __init__(self, path: str,  file_desc: str, object_desc: List[str] = None):
        self.path = path
        self.file_desc = file_desc
        self.object_desc = object_desc

    def add_object_desc(self, desc):
        self.object_desc.append(desc)

    def __str__(self):
        return f"DescriptedFile(path:{self.path} file_desc:{self.file_desc}, object_desc:{self.object_desc})"
