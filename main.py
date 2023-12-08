import config
from pinecone_manager import PineconeManager
from openai_asker import OpenaiAsker
from mongo_manager import MongoManager
from code_splitter import CodeSplitter
from langchain.embeddings import OpenAIEmbeddings

# Stwórz klase
splitter = CodeSplitter(config.PROJECT_REPO_LOCATION)

# Rozdziel pliki na pomniejsze kawałki tekstu
split_contents = splitter.to_indexed_objects()
CodeSplitter.print_indexed_objects(split_contents)

pinecone_mgr = PineconeManager(config.PINECONE_INDEX_NAME, True)
pinecone_mgr.index_content(split_contents)

index = pinecone_mgr.get_index()

mongo_mgr = MongoManager("test-session")

ai_asker = OpenaiAsker(index)
#result = ai_asker.ask("Give me the contents of the file with path 'P:\\Files\\Python\\llm\\_AuxiliaryProjects\\GitEasyClasses\\monitor.py'")
#print(result)

result = ai_asker.ask("Add a parameter ram to the class Computer and return the whole class with the changes")

docsearch = pinecone_mgr.get_index()
docs = docsearch.similarity_search_with_score("Add a parameter ram to the class Computer and return the whole class with the changes")
print(docs)
result = ai_asker.ask("What did I ask about a moment ago?")