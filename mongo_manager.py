import os

from langchain.memory import ConversationBufferMemory, MongoDBChatMessageHistory


class MongoManager:

    def __init__(self, session_id, api_key):
        self.session_id = session_id
        self.api_key = api_key
        self.message_history = MongoDBChatMessageHistory(
            connection_string=api_key,
            session_id=self.session_id
        )

    def add_message_to_Mongo(self, user_message, ai_message):
        self.message_history.add_user_message(user_message)
        self.message_history.add_ai_message(ai_message)

