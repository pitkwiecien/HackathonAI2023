from langchain.tools import BaseTool
from globals import Globals
import config
from pinecone_manager import PineconeManager
from openai_asker import OpenaiAsker
from mongo_manager import MongoManager
from code_splitter import CodeSplitter
from objects.indexed_object import IndexedObject
from file_descriptor import FileDescriptor
from code_descriptor import CodeDescriptor
from git_manager import GitManager
from descripted_file import DescriptedFile


class DocumentTool(BaseTool):
    """
    A tool designed to generate documentation for code when prompted.

    Attributes:
    - name (str): Name of the tool.
    - description (str): Description of the tool.
    """

    name: str = "DescriptionTool"
    description: str = "Use this tool only when asked to document code."

    def _run(self, query: str) -> str:
        """
        Runs the DocumentTool to create documentation for code.

        Args:
        - query (str): The query to trigger the documentation process.

        Returns:
        - str: Confirmation message after generating documentation at the project location.
        """

        # Setting the default message
        Globals.used_tool_message = "Documentation created at project location"

        # Splitting code contents into IndexedObjects
        splitter = CodeSplitter(config.PROJECT_REPO_LOCATION)
        split_contents = splitter.to_indexed_objects()

        # Fetching paths and creating IndexedObjects for files
        paths = GitManager.get_all_files_in_directory(config.PROJECT_REPO_LOCATION)
        new_paths = [IndexedObject.create_object("", path=path) for path in paths]

        # Describing files using FileDescriptor
        file_descriptor = FileDescriptor(new_paths)
        desc_file = file_descriptor.describe()

        # Creating a code descriptor using CodeDescriptor
        code_descriptor = CodeDescriptor(split_contents, desc_file)
        desc_code = code_descriptor.describe()

        # Initializing documents with DescriptedFile and creating documentation
        DescriptedFile.initialize_documents(DescriptedFile.get_ai_doc_location(), desc_code)

        return "Documentation created at project location"
