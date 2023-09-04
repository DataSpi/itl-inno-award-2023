""" 
This is inspired by a tutorial: https://www.youtube.com/watch?v=dXxQ0LR-3Hg&t=85s
Author: Spyno

Note: 2023-21-7 20:50 ValueError: Error raised by inference API: Input validation error: `inputs` must have less than 1024 tokens. Given: 1531
"""
# conda install -c conda-forge streamlit pypdf2 langchain python-dotenv faiss-cpu openai huggingface_hub

import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceInstructEmbeddings
# from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
# from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub


def get_pdf_text(pdf_docs): 
    """_summary_
    timestamp: phút 21 đến 25
    """
    text = ""
    for pdf in pdf_docs: 
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages: 
            text += page.extract_text() 
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n", 
        chunk_size = 1000, 
        chunk_overlap = 200, 
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks 

def get_vectorstore(text_chunks): # choose the embedding model (OpenAI or HuggingFace)
    # embeddings = OpenAIEmbeddings() # using OpenAI
    embeddings = HuggingFaceInstructEmbeddings(model_name = "hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore): # choos the llm here
    # llm = ChatOpenAI()
    llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = llm, 
        retriever = vectorstore.as_retriever(), 
        memory = memory
    )
    return conversation_chain

def handle_user_input(user_question): # minute 58th tutorial
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']
    
    for i, message in enumerate(st.session_state.chat_history): 
        if i % 2 == 0: 
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else: 
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

def main():
    load_dotenv()
    st.set_page_config(page_title = "Chat with multiple PDFs", page_icon=":books")
    st.write(css, unsafe_allow_html=True)
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = None 
    if "chat_history" not in st.session_state: 
        st.session_state.chat_history = None
    
    st.header("The chatbot that explain all ITL HR's Policies")
    user_question = st.text_input("Ask question about ITL's HR Policies")
    if user_question: 
        handle_user_input(user_question)
    
    st.write(user_template.replace("{{MSG}}", "Hello Robot!"), unsafe_allow_html=True)
    st.write(bot_template.replace("{{MSG}}", "Hello Human!"), unsafe_allow_html=True)
    
    with st.sidebar: # if you want to put things inside the sidebar, you have to do 'with'
        st.subheader("Your document")
        pdf_docs = st.file_uploader(
            label="Upload your PDFs here and Click on Process", 
            accept_multiple_files=True
            )
        if st.button("Process"):
            with st.spinner("Processing"):  # this is for user experience, they'll a spinning wheel
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)
                
                # get the text chunks
                text_chunks = get_text_chunks(raw_text)
                # st.write(text_chunks)
                
                # create vector store 
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)


# I have to learn about the backend of langchain later
# timestamp: phút 11 đến 16
        
if __name__ == '__main__':
    main()
        
