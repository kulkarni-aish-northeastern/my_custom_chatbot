import os
import sys
import openai
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.document_loaders import CSVLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma
from dotenv import load_dotenv

# This sets the environment variable for the OpenAI API key.
load_dotenv(".env")
openai.api_key = os.getenv("OPENAI_API_KEY")

# It creates a DirectoryLoader object that will load the documents from the `docs/` directory.
loader = DirectoryLoader("docs/", glob='**/*.csv', show_progress=True, loader_cls=TextLoader, use_multithreading=True)

#It creates a VectorstoreIndexCreator object and uses it to create a vectorstore index from the documents loaded by the DirectoryLoader object.
index = VectorstoreIndexCreator().from_loaders([loader])

# This function takes a message as input and returns the answer from the ChatOpenAI model.
def answer(msg):
  PERSIST = False
  query = None
  if len(sys.argv) > 1:
    query = sys.argv[1]

  # This creates a ConversationalRetrievalChain object that uses the ChatOpenAI model and the index created in the previous step.
  chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(model="gpt-3.5-turbo"),
    retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
  )
  chat_history = []
  query = msg

 # This runs the chain and returns the answer from the ChatOpenAI model.
  result = chain({"question": query, "chat_history": chat_history})
  return  result['answer']

if __name__ == "__main__":
  print ("haha")

