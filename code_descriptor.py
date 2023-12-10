from typing import List
from descripted_file import DescriptedFile
from objects.indexed_object import IndexedObject
from openai_asker import OpenaiAsker


class CodeDescriptor:
    """
    A class to describe code elements and associate descriptions with code objects.

    Attributes:
    - docs (List[IndexedObject]): List of IndexedObject instances representing code elements.
    - files (List[DescriptedFile]): List of DescriptedFile instances containing code descriptions.
    """

    def __init__(self, docs: List[IndexedObject], files: List[DescriptedFile]):
        """
        Initializes the CodeDescriptor with IndexedObject instances and DescriptedFile instances.

        Args:
        - docs (List[IndexedObject]): List of IndexedObject instances representing code elements.
        - files (List[DescriptedFile]): List of DescriptedFile instances containing code descriptions.
        """
        self.docs = docs
        self.files = files

    def describe(self):
        """
        Associates descriptions with code elements and files.

        Returns:
        - List[DescriptedFile]: List of DescriptedFile instances containing updated code descriptions.
        """
        docsize = len(self.docs)
        i = 0
        for doc in self.docs:
            print("DESCRIBING CODE {index} of {size}".format(index=i,size=docsize))
            i += 1
            print("||=============||")
            matching_field = None
            print(f"path to find: {doc.metadata['path']}")
            for f in self.files:
                test = f.path.replace('\\\\','\\')
                if test == doc.metadata["path"]:
                    matching_field = f
                    break
            doc.metadata["meaning"] = matching_field.file_desc
            result = OpenaiAsker.describe_code(doc)
            print(result)
            if matching_field:
                matching_field.add_object_desc(result)
        return self.files

