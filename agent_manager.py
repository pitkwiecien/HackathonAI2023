import os
from globals import Globals

from langchain.agents import tool, initialize_agent
from langchain.memory import ConversationBufferMemory
from mongo_manager import MongoManager
from langchain.llms import OpenAI
from tools.documentation_tool import DocumentTool
from tools.not_implemented_tool import NotImplementedTool
from langchain.load.dump import dumps


class AgentManager:
    used_tool = None

    def __init__(self, mongo_api_key):
        llm = OpenAI(temperature=0)
        tools = [NotImplementedTool(), DocumentTool()]
        self.memory = ConversationBufferMemory(
                    memory_key="chat_history",
                    return_messages=True
                )
        # self.mongo_manager = MongoManager('agent-session', mongo_api_key)
        self.agent = initialize_agent(tools=tools, llm=llm, verbose=False, max_iterations=1)

    def run_agent(self, prompt):
        self.agent({"input": prompt})
        self.memory.save_context({"input": prompt}, {"output": Globals.used_tool_message})
        # self.mongo_manager.add_message_to_mongo(prompt, result)
        return Globals.used_tool_message


