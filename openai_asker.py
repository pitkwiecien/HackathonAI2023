from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.callbacks import StdOutCallbackHandler
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import SystemMessage

from objects.indexed_object import IndexedObject
from descripted_file import DescriptedFile


class OpenaiAsker:
    def __init__(self, index, chain_type="stuff"):
        self.index = index
        print(self.index)
        self.chain_type = chain_type
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

    def ask_index(self, query):
        template = """
You will be given tasks to perform on given python code. Answer them by performing given actions and returning the updated version
of the code including the whole changed object. Return the objects that you think should be changed in the updated version. If one or more of these objects 
had been changed before and appear in Context, perform any changes considering the previous changes.

Context: 
{context}

{format_instructions}

Human: {question}

Helpful Assistant:
        """

        response_schemas = [
            ResponseSchema(name="new code", description="This is an updated version of the code"),
            ResponseSchema(name="path", description="This is the value \"path\" in question metadata")
        ]

        parser = StructuredOutputParser.from_response_schemas(response_schemas)

        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=template,
            partial_variables={
                "format_instructions": parser.get_format_instructions()
            }
        )

        chain = RetrievalQA.from_chain_type(
            llm=OpenAI(temperature=0),
            retriever=self.index.as_retriever(),
            memory=self.memory,
            chain_type="stuff",
            chain_type_kwargs={'prompt': prompt},
            callbacks=[StdOutCallbackHandler()]
        )

        # noinspection PyUnresolvedReferences
        msg = chain.memory.chat_memory.messages
        context = self.format_to_context(msg)
        # print(context)

        # noinspection PyUnresolvedReferences
        print(prompt.format_prompt(context=context, question=query).text)

        output = chain({"query": query})

        return output

    @staticmethod
    def print_answer(answer):
        for key, value in answer.items():
            print(f"{key}: ")
            if type(value) == list:
                for elem in value:
                    print(elem)
            else:
                print(value)

    @staticmethod
    def format_to_context(history):
        eq = ""
        for i in range(len(history)//2):
            eq += f"Human: {history[i*2].content}\n"
            eq += f"Assistant: {history[i*2 + 1].content}\n"
        return eq

    @staticmethod
    def get_result_from_answer(answer):
        return answer["result"]

    @staticmethod
    def describe_file(param: IndexedObject):
        template = ChatPromptTemplate.from_messages([
            SystemMessage(content=("You are a django assistant that explains the meaning of files in a"
                                  "django project. Your answers have to be short (max 3 sentences)")),
            HumanMessagePromptTemplate.from_template("{path}")
        ])
        llm = ChatOpenAI(temperature=0)
        return llm(template.format_messages(path=param.metadata["path"])).content

    @staticmethod
    def describe_code(param: IndexedObject):
        template = ChatPromptTemplate.from_messages([
            SystemMessage(content=("You are a helpful assistant that explains the meaning of classes in a"
                                   "django project. Your answers have to be short."
                                   "Consider the meaning of the file in the context of django, but "
                                   "focus mainly on the description of it. You have to shortly "
                                   "explain the object's parameters if there are any, its functions if "
                                   "it is a class."
                                   "Meaning of the file it is in: {meaning}")),
            HumanMessagePromptTemplate.from_template("{code}")
        ])
        llm = ChatOpenAI(temperature=0)
        description = llm(template.format_messages(code=param.data, meaning=param.metadata["meaning"])).content
        return description


