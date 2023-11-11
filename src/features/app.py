import streamlit as st
import os
import pinecone
from langchain.llms import OpenAI
from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from dotenv import load_dotenv
load_dotenv()



# ================================seting up pinecone================================
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment='gcp-starter'# this thing can be found at your acc at https://app.pinecone.io/
)

index_name = "itl-knl-base"
embeddings = OpenAIEmbeddings()
docsearch = Pinecone.from_existing_index(index_name, embeddings)



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



# ================================STREAMLIT APP================================
st.title('🦜🔗 ITL Internal Assistant Demo')



with st.form('my_form'):
    user_question = st.text_area('Enter text:', 'What can I wear in the office?')
    submitted = st.form_submit_button('Submit')
    if submitted:
        # generate_response(text)
        answer = qa(user_question=user_question)
        st.write(answer)
