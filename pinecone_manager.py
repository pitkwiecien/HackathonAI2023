import os

# noinspection PyPackageRequirements
import pinecone
# noinspection PyPackageRequirements
from pinecone.core.client.exceptions import NotFoundException, ApiException
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.schema import Document


class PineconeManager:
    __instance = None

    def __init__(self, index_name, api_key, insta_delete=False):
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
        if not cls.__instance:
            cls.__instance = super(PineconeManager, cls).__new__(cls)
        return cls.__instance

    def index_content(self, content):
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
        embeddings_model = OpenAIEmbeddings()
        return Pinecone.from_existing_index(self.index_name, embeddings_model)

    @classmethod
    def content_for_pinecone(cls, indexed_object_list):
        return tuple(map(lambda x: Document(page_content=x.data, metadata=x.metadata), indexed_object_list))
