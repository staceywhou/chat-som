import os
import key
import tabulate
# Set API keys from environment variables
os.environ["OPENAI_API_KEY"] = key.OPENAI_API_KEY

#Import relevant libraries
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import CSVLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.vectorstores import DocArrayInMemorySearch

#Reading in the file
file = '/workspaces/chat-som/chat_som/course_list/courseslist.csv'
loader = CSVLoader(file_path=file, encoding='utf-8')
data = loader.load()

#Creating a vector store and index using DocArrayInMemory Search---Automated chunking by Rows in CSV file
index = VectorstoreIndexCreator(
    vectorstore_cls=DocArrayInMemorySearch
).from_loaders([loader])

#Setting up the QA retreival chain

llm = ChatOpenAI(temperature = 0.0)
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=index.vectorstore.as_retriever(),
    verbose=False,
    chain_type_kwargs = {
        "document_separator": "<<<<>>>>>"
    }
)

def chat(user_message):
    """Get a message from user and generate a response"""
    response = qa.run(user_message)
    return response