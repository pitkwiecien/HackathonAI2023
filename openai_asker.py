from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.callbacks import StdOutCallbackHandler
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory


class OpenaiAsker:
    def __init__(self, index, chain_type="stuff"):
        self.index = index
        self.chain_type = chain_type
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )

    def ask(self, query):
        template = """
You will be given tasks to perform on given python code. Answer them by performing given actions and returning the updated version
of the code including the whole changed object. Return the objects that you think should be changed in the updated version. If one or more of these objects 
had been changed before and appear in Context, perform any changes considering the previous changes.

Context: 
{context}

Human: {question}

Assistant:
        """

        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=template
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
        print(context)

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
