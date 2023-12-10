import os

# noinspection PyPackageRequirements
import pinecone
# noinspection PyPackageRequirements
from pinecone.core.client.exceptions import NotFoundException, ApiException
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.schema import Document


class PineconeManager:
    """
    A singleton class managing interactions with Pinecone for indexing and retrieval.

    Attributes:
    - index_name (str): Name of the Pinecone index.

    Methods:
    - __init__(index_name, api_key, insta_delete=False): Initializes the PineconeManager with index_name, API key, and insta_delete flag.
    - index_content(content): Indexes content in Pinecone.
    - get_index(): Retrieves the Pinecone index.
    - content_for_pinecone(indexed_object_list): Formats content for indexing in Pinecone.
    """
    __instance = None

    def __init__(self, index_name, api_key, insta_delete=False):
        """
        Initializes the PineconeManager with index_name, API key, and insta_delete flag.

        Args:
        - index_name (str): Name of the Pinecone index.
        - api_key (str): API key for Pinecone.
        - insta_delete (bool): Flag for instant deletion. Defaults to False.
        """
        self.index_name = index_name
        pinecone.init(environment='gcp-starter', api_key=api_key)
        if insta_delete:
            try:
                pinecone.delete_index(index_name)
            except Exception:  # noqa
                pass
        try:
            _ = pinecone.describe_index(index_name)
            
        except NotFoundException:
            try:
                pinecone.create_index(index_name, 1536)
                
            except ApiException:
                indices = pinecone.list_indexes()
                for index in indices:
                    pinecone.delete_index(index)
                pinecone.create_index(index_name, 1536)

    def __new__(cls, *args, **kwargs):
        """
        Overrides the __new__ method to ensure a singleton instance of PineconeManager.

        Returns:
        - PineconeManager: The singleton instance of the class.
        """
        if not cls.__instance:
            cls.__instance = super(PineconeManager, cls).__new__(cls)
        return cls.__instance

    def index_content(self, content):
        """
        Indexes content in Pinecone.

        Args:
        - content: Content to be indexed.
        """
        embeddings_model = OpenAIEmbeddings()
        index = pinecone.Index(self.index_name)
        index.delete(delete_all=True)

        content_formatted = self.content_for_pinecone(content)
        # print("++++++++++++++++++++")
        # print(content_formatted[0].metadata)
        Pinecone.from_documents(
            content_formatted,
            embeddings_model,
            index_name=self.index_name
        )

    def get_index(self):
        """
        Retrieves the Pinecone index.

        Returns:
        - Pinecone index: The retrieved Pinecone index.
        """
        embeddings_model = OpenAIEmbeddings()
        return Pinecone.from_existing_index(self.index_name, embeddings_model)

    @classmethod
    def content_for_pinecone(cls, indexed_object_list):
        """
        Formats content for indexing in Pinecone.

        Args:
        - indexed_object_list: List of IndexedObject instances.

        Returns:
        - tuple: Formatted content for indexing in Pinecone.
        """
        return tuple(map(lambda x: Document(page_content=x.data, metadata=x.metadata), indexed_object_list))
