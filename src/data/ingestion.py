import pinecone
import os
from dotenv import load_dotenv
load_dotenv("/Users/spinokiem/Documents/Spino_DS_prj/building_a_chatbot")
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.document_loaders import TextLoader, Docx2txtLoader, UnstructuredExcelLoader, DataFrameLoader

# -------setting up the embedder & vectordatabase-------
embedder = OpenAIEmbeddings()
pinecone.init(api_key=os.getenv("PINECONE_API_KEY"), 
              environment='gcp-starter' # this thing can be found at your acc at https://app.pinecone.io/
            )
# pinecone.list_indexes()


# -------loading document-------
import pandas as pd
nqld=pd.read_excel("../../data/interim/nqld.xlsx")
rename_dict={
  'h1':'heading 1', 
  'h2':'heading 2',
  'h3':'heading 3'
}
nqld.rename(columns=rename_dict, inplace=True)
nqld.fillna("", inplace=True)
# nqld['metadata']=nqld[['heading 1', 'heading 2', 'heading 3']].to_dict(orient='records')
# # Format 'metadata' column as a list of dictionaries, removing NaN values
# nqld['metadata'] = [
#     [{col: value} for col, value in row.items() if not pd.isna(value)]
#     for row in nqld[['heading 1', 'heading 2', 'heading 3']].to_dict(orient='records')
# ]

# document_loader
loader = DataFrameLoader(nqld)
documents = loader.load()
documents[0]
