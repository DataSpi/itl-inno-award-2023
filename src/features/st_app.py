# import streamlit as st
import os
import pinecone
from langchain.llms import OpenAI
from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from dotenv import load_dotenv

load_dotenv()

# load pinecone
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment='gcp-starter' # this thing can be found at your acc at https://app.pinecone.io/
)

index_name = "itl-knl-base"
embeddings = OpenAIEmbeddings()

# dir(Pinecone)
# doc=Pinecone.get_pinecone_index(index_name)
# dir(doc)
# doc.describe_index_stats()

docsearch = Pinecone.from_existing_index(index_name, embeddings)
# dir(docsearch)


print(docsearch.similarity_search("số ngày nghỉ có tăng theo thâm niên làm việc không?", k=3))
