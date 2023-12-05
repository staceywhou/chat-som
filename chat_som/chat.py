# integrate chat gpt into the app

#integrate the main app
from flask import redirect, render_template, session
from functools import wraps
import key
import os
import openai
import textwrap
import pandas as pd
import csv

# Libraries for Document Splitting, embeddings, and vector stores
from langchain.document_loaders import CSVLoader
from langchain.docstore.document import Document
#from langchain.text_splitter import SimpleTextSplitter  # Change to SimpleTextSplitter
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma

# Chain for Q&A after retrieving external documents
from langchain.chains import RetrievalQA

# Using ChatOpenAI
from langchain.chat_models import ChatOpenAI

# define columns to embed vs columns that are meta data
columns_to_embed = ["Course Number","Course Description"]
columns_to_metadata = ["Course Category","Course ID", "Course Session","Course Title", "Daytimes", "Faculty 1"]


# OpenAI Key
openai.api_key = key.OPENAI_API_KEY
os.environ["OPENAI_API_KEY"]=key.OPENAI_API_KEY
apikey = key.OPENAI_API_KEY

csv_file_path = "course_list/courseslist.csv"  # Replace with your CSV file path
loader = CSVLoader(csv_file_path)
documents = loader.load()
print(documents)
print('\n')

# Process the CSV into the embedable content vs the metadata and put it into Document format so that we can chunk it into pieces.
docs = []
with open(csv_file_path, newline="", encoding='utf-8-sig') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for i, row in enumerate(csv_reader):
        to_metadata = {col: row[col] for col in columns_to_metadata if col in row}
        values_to_embed = {k: row[k] for k in columns_to_embed if k in row}
        to_embed = "\n".join(f"{k.strip()}: {v.strip()}" for k, v in values_to_embed.items())
        newDoc = Document(page_content=to_embed, metadata=to_metadata)
        docs.append(newDoc)


# Lets split the document using Chracter splitting. 
splitter = CharacterTextSplitter(separator = "\n",
                                chunk_size=500, 
                                chunk_overlap=0,
                                length_function=len)
chunks = splitter.split_documents(docs)

print(chunks[0])


# Store the chunks as embeddings within a vector store from which to retrieve information for queries
embeddings = OpenAIEmbeddings()
vector_store = Chroma.from_documents(chunks, embeddings)

# Initialize OpenAI instance and set up a chain for Q&A from an LLM and a vector score
llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0)
retriever = vector_store.as_retriever()
qachain = RetrievalQA.from_chain_type(llm, retriever=retriever)

# Run chain with question
question = "How many courses are in the dataset?"
response = qachain.run(question)
print(question)
print(textwrap.fill(response, 75))
print('\n')


# old code

def get_completion(prompt, model="gpt-3.5-turbo"):
  messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
      ]
  response = openai.ChatCompletion.create(
  model=model,
  messages=messages,
  )

  return(response['choices'][0]['message']['content'])


def get_completion_from_messages(messages, temperature, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
    #print(str(response.choices[0].message))
    return(response.choices[0].message["content"])


