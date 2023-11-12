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



# ================================seting up OpenAI================================
prompt_template = """You are an expert about policies of ITL Corporation, I will ask you a question, and then provide you some chunks of text contain relevant information about the question. 
Try to answer the question based on the text provided in Vietnamese.
Questions: 
{user_question}  

Relevant Information:
{relevant_info}
"""

llm = OpenAI(temperature=0)
llm_chain = LLMChain(
    llm=llm,
    prompt=PromptTemplate.from_template(prompt_template)
)



# ================================defining neccessary functions================================
def qa(user_question):
    """_summary_
    Query data from Pinecone database and then feed it to GPT using the prompt template
    """
    
    # query data
    top_k=docsearch.similarity_search_with_score(query=user_question, k=3)
    page_content=[i[0].page_content for i in top_k]

    # feed to GPT
    response = llm_chain(
        {
            'user_question': user_question,
            'relevant_info': page_content
        }
    )
    return response['text']


# def get_conversation_chain(vectorstore):
#     llm = ChatOpenAI()
#     memory = ConversationBufferMemory(
#         memory_key='chat_history', return_messages=True
#     )
#     conversation_chain = ConversationalRetrievalChain.from_llm(
#         llm=llm,
#         retriever=vectorstore.as_retriever(),
#         memory=memory
#     )
#     return conversation_chain

# conversation_chain=get_conversation_chain(vectorstore=docsearch)
# query = "số ngày nghỉ có tăng theo thâm niên làm việc không?"
# result = conversation_chain({"question": query})
# print(result['answer'])



# def handle_userinput(user_question):
#     response = st.session_state.conversation({'question': user_question})
#     st.session_state.chat_history = response['chat_history']

#     for i, message in enumerate(st.session_state.chat_history):
#         if i % 2 == 0:
#             st.write(user_template.replace(
#                 "{{MSG}}", message.content), unsafe_allow_html=True)
#         else:
#             st.write(bot_template.replace(
#                 "{{MSG}}", message.content), unsafe_allow_html=True)




# ================================STREAMLIT APP================================
import streamlit as st
import random
import time


st.title("ITL Internal AI Assistant 🤖")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages: 
    with st.chat_message(message["role"]):
        st.markdown(message['content'])

# # Ramdom greeting message:
# with st.chat_message("assistant"):
#     message_placeholder = st.empty()
#     full_response = ""
#     assistant_response = random.choice(
#         [
#             "Hello there! I am ITL BOT, an Artificial Intelligent developed by ITL Corporation. How can I assist you today?",
#             "Hi, ITL-ers! Is there anything ITL BOT can help you with?",
#             "Do you have any document you want me to find for you?",
#         ]
#     )
#     for chunk in assistant_response.split():
#         full_response += chunk + " "
#         time.sleep(0.05)
#         # Add a blinking cursor to simulate typing
#         message_placeholder.markdown(full_response + "▌")
#     message_placeholder.markdown(full_response)
# # Add assistant response to chat history
# st.session_state.messages.append({"role": "assistant", "content": full_response})


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
        full_response = ""
        assistant_response = qa(user_question=prompt)
        
        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    
