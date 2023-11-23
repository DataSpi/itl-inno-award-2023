import pandas as pd
from langchain.document_loaders import DataFrameLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
import pinecone
import os
from dotenv import load_dotenv
load_dotenv("/Users/spinokiem/Documents/Spino_DS_prj/building_a_chatbot")




# -------loading document-------
# nqld = pd.read_excel("../../data/interim/nqld.xlsx")
tuldtt = pd.read_excel("../../data/interim/tuldtt.xlsx")
tuldtt.text.str.len().mean()

rename_dict = {
    'h1': 'heading 1',
    'h2': 'heading 2',
    'h3': 'heading 3'
}
tuldtt.rename(columns=rename_dict, inplace=True)
tuldtt.fillna("", inplace=True)
# tuldtt['document'] = 'HR.03.V3.2023. Nội quy Lao động'

# use DataFrameLoader of langchain to create a `langchain.schema.document.Document` object
loader = DataFrameLoader(tuldtt)
documents = loader.load()
# type(documents[0])




# -------setting up the embedder & vectordatabase-------
embedder = OpenAIEmbeddings()
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment='gcp-starter' # environment's name can be found at your acc at https://app.pinecone.io/
)

index_name = "itl-knl-base"
if index_name not in pinecone.list_indexes():
    pinecone.create_index(
        name=index_name,
        metric='cosine',
        dimension=1536
    )


# if you already have an index, you can load it using Langchain like this
docsearch = Pinecone.from_existing_index(index_name, embedder)
docsearch.add_documents(documents)
# docsearch.__dir__()




# -------testing-------
# knl_base = pinecone.Index('itl-knl-base')
# knl_base.describe_index_stats()

# docsearch.similarity_search("quà mừng sinh nhật cho người lao động", k=3)