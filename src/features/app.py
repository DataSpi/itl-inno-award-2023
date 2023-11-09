"""
source: https://github.com/alejandro-ao/ask-multiple-pdfs/blob/main/app.py
tutorial: https://www.youtube.com/watch?v=dXxQ0LR-3Hg&list=WL&index=6
"""
import pandas as pd
import os
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader, PdfFileReader
# import PyPDF2
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub
from langchain.vectorstores import Pinecone
import pinecone
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment='gcp-starter' # environment's name can be found at your acc at https://app.pinecone.io/
)

def get_text(files):
    """
    Get text from .pdf, .txt, .xlsx
    """
    text = ""
    for file in files:
        if file.name.endswith('.pdf'):
            pdf_reader = PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        elif file.name.endswith('.txt'):
            text += file.read().decode('utf-8')
        elif file.name.endswith('.xlsx'):
            csv_file = file.name.replace('.xlsx', '.csv')
            df = pd.read_excel(file)
            df.to_csv(csv_file, index=False)
            
            loader = CSVLoader(file_path=csv_file)
            documents = loader.load()
            text=[i.page_content for i in documents]            
            # Delete the temporary CSV file
            os.remove(csv_file)
    return text


def get_text_chunks(text):
    """
    Splitting text into smaller chunks
    """
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks



def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    # embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl") # actually, I've searched on google, youtube. I think this is a pretty good model to embed text for semantic search, I think I don't need to find another model 
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    # model_name="google/flan-t5-xxl"
    # llm = HuggingFaceHub(repo_id=model_name, model_kwargs={"temperature":0.5, "max_length":512})
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)


# def main():
#     load_dotenv()
#     st.set_page_config(page_title="ITL Knowledge Base",
#                        page_icon=":books:")
#     st.write(css, unsafe_allow_html=True)
#     # st.write(f'We are using the model: {model_name}')

#     if "conversation" not in st.session_state:
#         st.session_state.conversation = None
#     if "chat_history" not in st.session_state:
#         st.session_state.chat_history = None

#     st.header("ITL Knowledge Base :books:")
#     user_question = st.text_input("Ask a question about company's policies:")
#     if user_question:
#         handle_userinput(user_question)

#     with st.sidebar:
#         st.subheader("Your documents")
#         files = st.file_uploader(
#             "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
#         if st.button("Process"):
#             with st.spinner("Processing"):
#                 # get pdf text
#                 raw_text = get_text(files)

#                 # chunk the text into smaller pieces
#                 text_chunks = get_text_chunks(raw_text)

#                 # create vector store
#                 vectorstore = get_vectorstore(text_chunks)
#                 vectorstore = pinecone.Index('itl-knl-base')
                

#                 # create conversation chain
#                 st.session_state.conversation = get_conversation_chain(
#                     vectorstore)

def main():
    load_dotenv()
    st.set_page_config(page_title="ITL Knowledge Base",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)
    # st.write(f'We are using the model: {model_name}')

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("ITL Knowledge Base :books:")
    user_question = st.text_input("Ask a question about company's policies:")
    if user_question:
        handle_userinput(user_question)

    # # load vector store
    # embeddings = OpenAIEmbeddings()
    # index_name = 'itl-knl-base'
    # vectorstore = Pinecone.from_existing_index(index_name, embeddings)
    
    # # create conversation chain
    # st.session_state.conversation = get_conversation_chain(
    #     vectorstore)



if __name__ == '__main__':
    main()




# # load vector store
# embeddings = OpenAIEmbeddings()
# index_name = 'itl-knl-base'
# vectorstore = Pinecone.from_existing_index(index_name, embeddings)
# get_conversation_chain(vectorstore=vectorstore)
# # create conversation chain
# st.session_state.conversation = get_conversation_chain(
#     vectorstore)
