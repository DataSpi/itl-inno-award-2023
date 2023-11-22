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
import pandas as pd
load_dotenv()
import json



# ================================seting up pinecone================================
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment='gcp-starter'# this thing can be found at your acc at https://app.pinecone.io/
)

index_name = "itl-knl-base"
embeddings = OpenAIEmbeddings()
docsearch = Pinecone.from_existing_index(index_name, embeddings) # this is the vectorstore
query="Thời giờ làm việc của nhân viên ITL"
# làm for loop, tinh similarity score trung binh

# ================================seting up OpenAI================================
prompt_template = """You are an expert about policies of ITL Corporation, I will ask you a question, and then provide you some chunks of text contain relevant information. 
Try to extract information from the provided text & answer in Vietnamese. 
You should answer straight to the point of the question, ignore irrelevant information, prefer bullet-points. 
If the text does not contain relevant information, you should tell me that you don't have the answer.

Questions:
{user_question}  

Relevant Information:
{relevant_info}
"""


llm = OpenAI(temperature=0, max_tokens=1024, model="text-davinci-002")
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
    metadata=[top_k[i][0].metadata for i in range(len(top_k))]

    # feed to GPT
    response = llm_chain(
        {
            'user_question': user_question,
            'relevant_info': page_content
        }
    )
    return response['text'], metadata


def similarity_search(user_question):
    top_k=docsearch.similarity_search_with_score(query=user_question, k=3)
    return top_k    


def parsing_top_k(top_k):
    """reading information from the top_k results"""
    page_content=[i[0].page_content for i in top_k]
    metadata=[top_k[i][0].metadata for i in range(len(top_k))]
    meta_list = ["/".join(i.values()) for i in metadata]
    
    return page_content, meta_list


def feed_ques2gpt(user_question, page_content):
    """feed the user_question & top_k result to GPT"""
    # feed to GPT
    response = llm_chain(
        {
            'user_question': user_question,
            'relevant_info': page_content
        }
    )
    return response['text']


# top_k=similarity_search(user_question=user_question)
# page_content, meta_list = parsing_top_k(top_k)
# response = feed_ques2gpt(user_question, page_content)



# ================================STREAMLIT APP================================
import streamlit as st
import random
import time
from datetime import datetime
from loguru import logger

log_name = "file_log.log"
logger.add(log_name)


streamlit_start_time = time.time()
dt = datetime.fromtimestamp(streamlit_start_time)
formatted_time = dt.strftime("%Y%m%d-%Hh%Mm%Ss")


st.title("ITL Internal AI Assistant 🤖")

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

# Check if greeting has been shown before
if "greeting_shown" not in st.session_state:
    st.session_state.greeting_shown = False

# Random greeting messages
if not st.session_state.greeting_shown:
    st.session_state.greeting_shown = True
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = random.choice(
            [
                "Hello there! I am ITL BOT, an Artificial Intelligent developed by ITL Corporation. How can I assist you today?",
                "Hi, ITL-ers! Is there anything ITL BOT can help you with?",
                "Hello! Do you have any question you want me to find answer for?",
            ]
        )
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    # Add assistant response to chat history
    st.session_state.messages = [{"role": "assistant", "content": full_response}]

# -----React to user input-----
# Initialize DataFrame to store data
data = {"user_ques": [], "top_k": [], "assistant_response": [], "metadata": [], "similarity_search_time": [], "feed_ques2gpt_time": []}
df = pd.DataFrame(data)


if user_ques := st.chat_input("Ask questions about ITL's policies"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_ques})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_ques)
    
    
    ###### processing & preparing data
    # search top_k & record time
    start_time_similarity_search = time.time()    
    top_k=similarity_search(user_ques)
    end_time_similarity_search = time.time()
    
    # parsing top_k
    page_content, metadata = parsing_top_k(top_k)
    
    # feed to gpt & record time
    start_time_feed_ques2gpt = time.time()
    assistant_response = feed_ques2gpt(user_ques, page_content)
    end_time_feed_ques2gpt = time.time()
    
    # # Save data to DataFrame
    # df = df.append({
    #     "user_ques": user_ques,
    #     "top_k": top_k,
    #     "assistant_response": assistant_response,
    #     "metadata": metadata,
    #     "similarity_search_time": end_time_similarity_search - start_time_similarity_search,
    #     "feed_ques2gpt_time": end_time_feed_ques2gpt - start_time_feed_ques2gpt
    # }, ignore_index=True)
    
    log_current = {
        "user_ques": user_ques,
        "top_k": top_k,
        "assistant_response": assistant_response,
        "metadata": metadata,
        "similarity_search_time": end_time_similarity_search - start_time_similarity_search,
        "feed_ques2gpt_time": end_time_feed_ques2gpt - start_time_feed_ques2gpt}
    
    logger.debug(str(log_current))
    
    
    ##### Display assistant response 
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        assistant_response = f"{assistant_response}\n\n**📌 Thông tin chi tiết, tham khảo:**\n\n*{metadata}*"
        
        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split(" "):
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Save DataFrame to CSV when the app stops
# if st.server.is_running:
# if st.running:
#     st.text("Streamlit app is still running. Stop the app to save data.")
# else:
#     df.to_csv(f"running-data{streamlit_start_time}.csv", index=False)
#     st.text("Data saved to 'your_data.csv'.")
