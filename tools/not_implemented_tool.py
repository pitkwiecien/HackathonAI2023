from langchain.tools import BaseTool
from globals import Globals


class NotImplementedTool(BaseTool):
    name: str = "notImplementedTool"
    description: str = "Use this tool when asked for writing code, tests or any other question. " \
                       "Do not use this tool if you are asked to document or describe code"

    def _run(self, query: str) -> str:
        Globals.used_tool_message = "Functionality has not been implemented yet"
        return "Functionality has not been implemented yet"
