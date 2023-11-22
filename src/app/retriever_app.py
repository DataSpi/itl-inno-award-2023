import streamlit as st
import os
import pinecone
from langchain.llms import OpenAI
from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from dotenv import load_dotenv
load_dotenv()



# ================================seting up pinecone================================
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment='gcp-starter'# this thing can be found at your acc at https://app.pinecone.io/
)

index_name = "itl-knl-base"
embeddings = OpenAIEmbeddings()
docsearch = Pinecone.from_existing_index(index_name, embeddings) # this is the vectorstore
# làm for loop, tinh similarity score trung binh





# ================================DEFINING FUNCTIONS================================
def search_vector(user_question):
    top_k=docsearch.similarity_search_with_score(query=user_question, k=3)
    page_content=[i[0].page_content for i in top_k]
    metadata=[top_k[i][0].metadata for i in range(len(top_k))]
    metadata = ["/".join(i.values()) for i in metadata]
    return page_content, metadata

user_question="Thời gian làm việc của nhân viên ITL"
top_k=docsearch.similarity_search_with_score(query=user_question, k=3)

content, meta = search_vector("Thời gian làm việc của nhân viên ITL")
meta="\n\n".join(meta)

for x, y in zip(content, meta):
    print(x)
    print(y)
    print("---")




# ================================STREAMLIT APP================================
import streamlit as st
import random
import time


st.title("ITL Information Retreiver Bot 🤖")

# Writing the disclaimer
style = """
    <style>
        .disclaimer {
            background-color: #2F2724;
            padding: 10px;
            color: #A9A9A9;
            font-style: italic;
            border-radius: 5px;
        }
    </style>
"""

st.write(style, unsafe_allow_html=True)

st.markdown("""
<details class="disclaimer">
    <summary><strong><em>⚠️ Note:</em></strong></summary>
     <p style="padding-left: 16px">Câu trả lời của AI chỉ mang tính chất tương đối. Đối với thông tin quan trọng, người dùng cần kiểm tra các tài liệu được dẫn nguồn.</p>
</details>
""", unsafe_allow_html=True)

# AI Assistant can make mistakes. Consider checking the provided source documents for important information.


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages: 
    with st.chat_message(message["role"]):
        st.markdown(message['content'])

# React to user input
if prompt := st.chat_input("Ask questions about ITL's policies"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response 
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        top_k, metadata = search_vector(user_question=prompt)
        full_response = f"{top_k}\n\n**📌 Thông tin chi tiết, xem thêm:**\n\n{metadata}"
        message_placeholder.markdown(full_response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})