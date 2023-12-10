from globals import Globals
from langchain.agents import initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI
from documentation_tool import DocumentTool
from not_implemented_tool import NotImplementedTool
from mongo_manager import MongoManager


class AgentManager:
    """
    A class managing the interaction between agents and tools.

    Attributes:
    - used_tool (None): Placeholder attribute to store the currently used tool.
    - memory (ConversationBufferMemory): Instance to manage conversation history.
    - agent: The initialized agent for interactions.
    """

    used_tool = None

    def __init__(self, mongo_api_key):
        """
        Initializes the AgentManager with required parameters.

        Args:
        - mongo_api_key (str): The API key for MongoDB.
        """
        llm = OpenAI(temperature=0)
        tools = [NotImplementedTool(), DocumentTool()]
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        # self.mongo_manager = MongoManager('agent-session', mongo_api_key)
        self.agent = initialize_agent(tools=tools, llm=llm, verbose=False, max_iterations=1)

    def run_agent(self, prompt):
        """
        Runs the agent with the provided prompt.

        Args:
        - prompt (str): The input prompt for the agent.

        Returns:
        - str: The message generated by the used tool.
        """
        self.agent({"input": prompt})
        self.memory.save_context({"input": prompt}, {"output": Globals.used_tool_message})
        # self.mongo_manager.add_message_to_mongo(prompt, Globals.used_tool_message)
        return Globals.used_tool_message
