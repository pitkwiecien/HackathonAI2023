import config
from git_manager import GitManager
from file_manager import FileManager
from pinecone_manager import PineconeManager
from openai_asker import OpenaiAsker
from mongo_manager import MongoManager

file_contents = GitManager.get_files_content(config.PROJECT_REPO_LOCATION)
split_contents = FileManager.split_content(file_contents)
# FileManager.print_split_file_content(split_contents)

pinecone_mgr = PineconeManager(config.PINECONE_INDEX_NAME)
pinecone_mgr.index_content(split_contents)

index = pinecone_mgr.get_index()

mongo_mgr = MongoManager("test-session")

ai_asker = OpenaiAsker(index)
result = ai_asker.ask("Add a parameter ram to the class Computer and return the whole class with the changes")
OpenaiAsker.print_answer(result)
result = ai_asker.ask("What did I ask about a moment ago?")
OpenaiAsker.print_answer(result)
