from langchain.document_loaders.csv_loader import CSVLoader
from langchain.document_loaders.word_document import Docx2txtLoader
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.text_splitter import CharacterTextSplitter

from dotenv import load_dotenv
load_dotenv()


loader= Docx2txtLoader(file_path="../../data/raw/6. HR.03.V3.2023. Nội quy Lao động_Review by Labor Department - Final.docx")
# 1. Vectorise the sales response csv data
# loader = CSVLoader(file_path="itl-testing.csv")
documents = loader.load()
text=documents[0].page_content
    # CSVLoader sẽ store mỗi dòng trong csv thành một điểm data. lúc mà vectorize là nó sẽ vectorize 1 dòng 

# embeddings = OpenAIEmbeddings() # oke, so, this step require me to have the chatgpt API.
embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl") # actually, I've searched on google, youtube. I think this is a pretty good model to embed text for semantic search, I think I don't need to find another model 
# embeddings = HuggingFaceInstructEmbeddings(model_name="Xenova/text-embedding-ada-002") 
# db = FAISS.from_documents(documents, embeddings)
# type(db) = langchain.vectorstores.faiss.FAISS



def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    # embeddings = OpenAIEmbeddings()
    embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl") # actually, I've searched on google, youtube. I think this is a pretty good model to embed text for semantic search, I think I don't need to find another model 
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


text_chunks=get_text_chunks(text=text)
len(text_chunks)

vectorstore=get_vectorstore(text_chunks=text_chunks)

# testing
query = "sa thải là điều thứ mấy"
responses=vectorstore.similarity_search(query=query, k=3)

for i in range(len(responses)):
    print("---")
    print(responses[i].page_content)

