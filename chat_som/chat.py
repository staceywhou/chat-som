import os
import key
import tabulate
# Set API key
os.environ["OPENAI_API_KEY"] = key.OPENAI_API_KEY

# Import langchain
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import CSVLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.vectorstores import DocArrayInMemorySearch

# Load the csv file
file = '/workspaces/chat-som/chat_som/course_list/courseslist.csv'
loader = CSVLoader(file_path=file, encoding='utf-8')
data = loader.load()

# chunk the data and import into arrays
index = VectorstoreIndexCreator(
    vectorstore_cls=DocArrayInMemorySearch
).from_loaders([loader])

# set up the retreival chain
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

# function that takes a message and returns a response
def chat(user_message):
    """Get a message from user and generate a response"""
    response = qa.run(user_message)
    return response