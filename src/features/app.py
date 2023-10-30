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
import tiktoken
import urllib3

# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# def get_text(files):
#     text = ""
#     for pdf in files:
#         pdf_reader = PdfReader(pdf)
#         for page in pdf_reader.pages:
#             text += page.extract_text()
#     return text # this function extract text from all pages of all the pdfs & store them in the `text` variable

# def get_text(files):
#     """
#     this function extract text from all pages of all the pdfs 
#     & store them in the `text` variable
#     """
#     text = ""
#     for file in files:
#         if file.name.endswith('.pdf'):
#             pdf_reader = PdfReader(file)
#             for page in pdf_reader.pages:
#                 text += page.extract_text()
#         elif file.name.endswith('.txt'):
#             with open(file, 'r') as txt_file:
#                 text += txt_file.read()
#         elif file.name.endswith('.csv'):
#             loader = CSVLoader(file_path=file)
#             documents = loader.load()
#             text=[i.page_content for i in documents]
#         elif file.name.endswith('.xlsx'):
#             csv_file = file.replace('.xlsx', '.csv')
#             df = pd.read_excel(file)
#             df.to_csv(csv_file, index=False)
#             loader = CSVLoader(file_path=csv_file)
#             documents = loader.load()
#             text=[i.page_content for i in documents]
#             # Delete the temporary CSV file
#             os.remove(csv_file)
#     return text



def get_text(files):
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
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


# The reason why I donot understand this while following the tutorial, is that I can not understand the concept of embedding. 
# now (4/9/2023) I understand the concept, so this all make sense now. I think I can modify the code & see what would happen. 
def get_vectorstore(text_chunks):
    # embeddings = OpenAIEmbeddings()
    embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl") # actually, I've searched on google, youtube. I think this is a pretty good model to embed text for semantic search, I think I don't need to find another model 
    # embeddings = HuggingFaceInstructEmbeddings(model_name="TheBloke/Yarn-Llama-2-7B-128K-GPTQ") # this does not work, I guess this model is not for embedding. 
    # embeddings = HuggingFaceInstructEmbeddings(model_name="shalomma/llama-7b-embeddings") # actually, it's hard to find an embedding model, so I think hkunlp/instructor-xl is a good one
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

# -----------------------------------Test-----------------------------------
# # read the pdf & try to see how the get_pdf_text() & get_text_chunk() work. 
# %cd "/Users/spinokiem/Documents/Spino_DS_prj/building_a_chatbot"
# # test_pdf=PdfFileReader("data/raw/bọn trẻ bây giờ sướng thế, sao cứ trầm cảm nhỉ.pdf")
# # test_text=test_pdf.getPage(0).extract_text()
test_text = open('../../data/raw/quy-dinh-tai-noi-lam-viec.txt', 'r').read()
test_text_chunks=get_text_chunks(test_text)
for i in range(0,3):
    print('---')
    print(test_text_chunks[i]) # now I know how the get_text_chunk() works


# excel_file_path='data/raw/itl-testing.xlsx'
csv_file_path='../../data/processed/itl-testing.csv'
# # Convert Excel to CSV
# df = pd.read_excel(excel_file_path)
# df.to_csv(csv_file_path, index=False) # oke, so by converting file like this I can work w utf-8 of vnese. & can change modify it as well. 

loader=CSVLoader(file_path=csv_file_path)
documents=loader.load()
text=[i.page_content for i in documents]
for i in range(0,3):
    print('---')
    print(text[i])
# %cd "/Users/spinokiem/Documents/Spino_DS_prj/building_a_chatbot/src/features"


test_vectorstore=get_vectorstore(test_text_chunks)
query="ripped pants"
page_array=test_vectorstore.similarity_search(query=query, k=3)
for page in page_array:
    print('---')
    print(page.page_content)

# from datasets import load_dataset

# dataset = load_dataset("tinhpx2911/wiki-vn-process")
# dataset['train']['text']

# -----------------------------------End Test-----------------------------------


# model_name="google/flan-t5-xxl" "PY007/TinyLlama-1.1B-step-50K-105b" "google/flan-t5-base"
model_name="google/flan-t5-xxl"
def get_conversation_chain(vectorstore):
    # llm = ChatOpenAI()
    llm = HuggingFaceHub(repo_id=model_name, model_kwargs={"temperature":0.5, "max_length":512})

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


def main():
    load_dotenv()
    st.set_page_config(page_title="ITL Knowledge Base",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)
    st.write(f'We are using the model: {model_name}')

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("ITL Knowledge Base :books:")
    user_question = st.text_input("Ask a question about company's policies:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        files = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                # get pdf text
                raw_text = get_text(files)

                # get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # create vector store
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(
                    vectorstore)


if __name__ == '__main__':
    main()
