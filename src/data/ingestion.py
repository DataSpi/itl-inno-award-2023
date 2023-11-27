import pandas as pd
from langchain.document_loaders import DataFrameLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
import pinecone
import os
from dotenv import load_dotenv
load_dotenv("/Users/spinokiem/Documents/Spino_DS_prj/building_a_chatbot")



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



# -------loading document-------
policy = pd.read_excel("../../data/interim/nqld.xlsx")
# policy = pd.read_excel("../../data/interim/tuldtt.xlsx")
# policy = pd.read_excel("../../data/interim/healthcare.xlsx")
policy.text.str.len().mean()

rename_dict = {
    'h1': 'heading 1',
    'h2': 'heading 2',
    'h3': 'heading 3'
}
policy.rename(columns=rename_dict, inplace=True)
policy.fillna("", inplace=True)
# tuldtt['document'] = 'HR.03.V3.2023. Nội quy Lao động'

# use DataFrameLoader of langchain to create a `langchain.schema.document.Document` object
loader = DataFrameLoader(policy)
documents = loader.load()
# type(documents[0])



# -------embedding document-------

# if this is the first time you create the index, you can create it from your langchain.document like this: 
# docsearch = Pinecone.from_documents(documents, embedder, index_name=index_name)

# if you already have an index, you can load it using Langchain like this
docsearch = Pinecone.from_existing_index(index_name, embedder)
docsearch.add_documents(documents)


# delete the index
# pinecone.delete_index("itl-knl-base") # delete index




# -------testing-------
knl_base = pinecone.Index('itl-knl-base')
knl_base.describe_index_stats()

# docsearch.similarity_search("quà mừng sinh nhật cho người lao động", k=3)