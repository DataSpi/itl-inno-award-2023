import pandas as pd
from langchain.document_loaders import DataFrameLoader
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
import os
from dotenv import load_dotenv
load_dotenv("/Users/spinokiem/Documents/Spino_DS_prj/building_a_chatbot")


# -------loading document-------
nqld = pd.read_excel("../../data/interim/nqld.xlsx")
nqld.text.str.len().mean()

""" 
trung bình một đoạn văn của mình là 400 kí tự quy đổi ra thành khoảng 100 token. 
cứ cho là tiếng việt nhiều hơn thì sẽ là 150 tokens đi. 

mỗi lần hỏi mình feed top_3 kết quả => 150 * 3 = 450 tokens

cộng thêm với user_question & prompt_template khoảng 500 kí tự, quy ra thành hẳn 200 tokens đi.

-> input của mình khoảng 650 tokens. 
-> output của mình cho khoảng 400 tokens thì mới đúng 1k tokens. 

nếu như vậy thì mình phải hỏi khoảng 1000 câu hỏi mới hết 1 đô. 
mà sao tối qua em hỏi có mấy câu nó đã hết 1 đô rồi??? # 22/11/2022

"""

rename_dict = {
    'h1': 'heading 1',
    'h2': 'heading 2',
    'h3': 'heading 3'
}
nqld.rename(columns=rename_dict, inplace=True)
nqld.fillna("", inplace=True)
nqld['document'] = 'HR.03.V3.2023. Nội quy Lao động'

# use DataFrameLoader of langchain to create a `langchain.schema.document.Document` object
loader = DataFrameLoader(nqld)
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

# -------testing-------
# docsearch = Pinecone.from_documents(documents, embedder, index_name=index_name)

# # pinecone.delete_index("itl-knl-base") # delete all
# knl_base = pinecone.Index('itl-knl-base')
# knl_base.describe_index_stats()
