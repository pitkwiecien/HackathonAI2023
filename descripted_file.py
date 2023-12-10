from typing import List
import os
import config
import shutil


class DescriptedFile:
    def __init__(self, path: str, file_desc: str, object_desc=None):
        if object_desc is None:
            object_desc = []
        self.path = path
        self.file_desc = file_desc
        self.object_desc = object_desc

    def add_object_desc(self, desc):
        self.object_desc.append(desc)

    def __str__(self):
        return f"DescriptedFile(path:{self.path} file_desc:{self.file_desc}, object_desc:{self.object_desc})"

    @staticmethod
    def insert_str(string, str_to_insert, index):
        return string[:index] + str_to_insert + string[index:]

    # Tworzy dokumentacje dla danego pliku
    def create_document(self):
        document_location = self.path
        # document_location = self.insert_str(document_location, "/.ai_docs", self.path.rfind('/'))
        document_location = document_location.replace(config.PROJECT_REPO_LOCATION, config.PROJECT_REPO_LOCATION + config.DOCS_FOLDER_NAME)
        mkdir_location = document_location[:document_location.rfind('/')]
        if not os.path.exists(mkdir_location):
            os.makedirs(mkdir_location)
        document_location = document_location.replace('.py', '.txt')
        f = open(document_location, "w+")
        f.write(self.file_desc)
        f.write("\n\n")
        for x in self.object_desc:
            f.write(x)
            f.write('\n')
        f.close()

    @staticmethod
    def initialize_documents(ai_doc_location, documents):
        try:
            shutil.rmtree(ai_doc_location)
        except FileNotFoundError:
            pass
        for dc in documents:
            dc.create_document()

    @staticmethod
    def get_ai_doc_location():
        return config.PROJECT_REPO_LOCATION + config.DOCS_FOLDER_NAME

