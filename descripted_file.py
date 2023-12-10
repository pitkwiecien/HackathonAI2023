from typing import List
import os
import config
import shutil


class DescriptedFile:
    """
    A class representing a file with descriptions for both the file itself and associated objects.

    Attributes:
    - path (str): The path of the file.
    - file_desc (str): Description of the file.
    - object_desc (List[str]): List of descriptions for objects in the file.
    """

    def __init__(self, path: str, file_desc: str, object_desc=None):
        """
        Initializes a DescriptedFile instance with path, file description, and optional object descriptions.

        Args:
        - path (str): The path of the file.
        - file_desc (str): Description of the file.
        - object_desc (List[str], optional): List of descriptions for objects in the file. Defaults to None.
        """
        if object_desc is None:
            object_desc = []
        self.path = path
        self.file_desc = file_desc
        self.object_desc = object_desc

    def add_object_desc(self, desc):
        """
        Adds an object description to the DescriptedFile's object_desc list.

        Args:
        - desc (str): Description of the object.
        """
        self.object_desc.append(desc)

    def __str__(self):
        """
        Returns a string representation of the DescriptedFile.

        Returns:
        - str: String representation of the DescriptedFile.
        """
        return f"DescriptedFile(path:{self.path} file_desc:{self.file_desc}, object_desc:{self.object_desc})"

    @staticmethod
    def insert_str(string, str_to_insert, index):
        """
        Inserts a string into another string at a specified index.

        Args:
        - string (str): The original string.
        - str_to_insert (str): The string to insert.
        - index (int): The index at which to insert the string.

        Returns:
        - str: The updated string after insertion.
        """
        return string[:index] + str_to_insert + string[index:]

    def create_document(self):
        """
        Creates a documentation file for the DescriptedFile.

        The documentation includes the file description and object descriptions, saved as an .md file.
        """
        document_location = self.path.replace(config.PROJECT_REPO_LOCATION, config.PROJECT_REPO_LOCATION + config.DOCS_FOLDER_NAME)
        mkdir_location = document_location[:document_location.rfind('/')]
        if not os.path.exists(mkdir_location):
            os.makedirs(mkdir_location)
        document_location = document_location[:document_location.rfind('.')] + ".md"
        with open(document_location, "w+") as f:
            f.write(self.file_desc)
            f.write("\n\n")
            for x in self.object_desc:
                f.write(x)
                f.write('\n')

    @staticmethod
    def initialize_documents(ai_doc_location, documents):
        """
        Initializes documentation for DescriptedFiles.

        Removes existing documentation and creates new documentation for the provided DescriptedFiles.

        Args:
        - ai_doc_location (str): Location for storing AI-generated documentation.
        - documents (List[DescriptedFile]): List of DescriptedFile instances to generate documentation for.
        """
        try:
            shutil.rmtree(ai_doc_location)
        except FileNotFoundError:
            pass
        for dc in documents:
            dc.create_document()

    @staticmethod
    def get_ai_doc_location():
        """
        Retrieves the location for AI-generated documentation.

        Returns:
        - str: Location for storing AI-generated documentation.
        """
        return config.PROJECT_REPO_LOCATION + config.DOCS_FOLDER_NAME
