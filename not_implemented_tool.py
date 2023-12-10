from langchain.tools import BaseTool
from globals import Globals

class NotImplementedTool(BaseTool):
    """
    A tool representing functionality that has not been implemented yet.

    Attributes:
    - name (str): Name of the tool.
    - description (str): Description of the tool's usage.

    Methods:
    - _run(query: str) -> str: Placeholder method indicating unimplemented functionality.
    """

    name: str = "notImplementedTool"
    description: str = "Use this tool when asked for writing code, tests or any other question. " \
                       "Do not use this tool if you are asked to document or describe code"

    def _run(self, query: str) -> str:
        """
        Placeholder method indicating unimplemented functionality.

        Args:
        - query (str): The query triggering the use of this tool.

        Returns:
        - str: Message indicating functionality has not been implemented yet.
        """
        Globals.used_tool_message = "Functionality has not been implemented yet"
        return "Functionality has not been implemented yet"
