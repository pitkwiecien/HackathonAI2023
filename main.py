import os

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
from agent_manager import AgentManager

from os.path import join, dirname
# noinspection PyPackageRequirements
from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

mongo_url = os.environ.get("MONGO_URL")
a = AgentManager(mongo_url)

print(a.run_agent("make documentation for this project"))

# Stwórz klase


# Rozdziel pliki na pomniejsze kawałki tekstu


# code_api = os.environ.get("PINECONE_CODE_API_KEY")
# print(code_api)
# print(config.PINECONE_CODE_INDEX_NAME)
# pinecone_mgr = PineconeManager(config.PINECONE_CODE_INDEX_NAME, os.environ.get("PINECONE_CODE_API_KEY"), True)
# pinecone_mgr.index_content(split_contents)
#
# index = pinecone_mgr.get_index()
#
# mongo_mgr = MongoManager("test-session")

# print(OpenaiAsker.describe_file(IndexedObject.create_object("", path="/templates/registration/login.html")))

# ai_asker = OpenaiAsker(index=index)
# result = ai_asker.ask_index("Describe to me file with the path 'P:\\Files\\Python\\llm\\_AuxiliaryProjects\\GitEasyClasses\\monitor.py'")
# print(result)

# result = ai_asker.ask_index("Add a parameter ram to the class Computer and return the whole class with the changes")
# print(OpenaiAsker.get_result_from_answer(result))

# docsearch = pinecone_mgr.get_index()
# docs = docsearch.similarity_search_with_score("Add a parameter ram to the class Computer and return the whole class with the changes")
# print(docs)
# result = ai_asker.ask_index("What did I ask about a moment ago?")
# print(OpenaiAsker.get_result_from_answer(result))
