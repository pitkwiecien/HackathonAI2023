import os
from agent_manager import AgentManager

from os.path import join, dirname
# noinspection PyPackageRequirements
from dotenv import load_dotenv


# Loading environment variables from .env file
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Retrieving the MongoDB URL from environment variables
mongo_url = os.environ.get("MONGO_URL")

# Initializing AgentManager with the MongoDB URL
a = AgentManager(mongo_url)

# Running the agent to trigger documentation creation for the project
print(a.run_agent("make documentation for this project"))
