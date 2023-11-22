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




# ================================seting up OpenAI================================
from langchain.prompts import PromptTemplate
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

system_template="""You are an expert about policies of ITL Corporation, I will ask you a question, and then provide you some chunks of text contain relevant information. 
Try to extract information from the provided text & answer in Vietnamese. 
You should answer straight to the point of the question, ignore irrelevant information, prefer bullet-points. 
If the text does not contain relevant information, you should tell me that you don't have the answer.
"""
human_template="""
Questions:
{user_question}  

Relevant Information:
{relevant_info}
"""
system_message_prompt = SystemMessagePromptTemplate.from_template(system_template)
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

chat = ChatOpenAI(temperature=0)

relevant_info="""
    .1 hoặc một số hành vi dưới đây: Không đúng giờ trong công việc, các buổi họp kinh doanh và/hoặc các khóa tập huấn mà không có lý do chính đáng; Không thông báo trong thời gian sớm nhất có thể được cho người quản lý trực tiếp của mình hoặc người được người quản lý trực tiếp ủy quyền khi Người Lao Động vắng mặt do bị ốm đau hoặc tai nạn hoặc vì bất kỳ lý do nào khác; Làm việc ít giờ hơn khi chưa được phép, cắt ngắn thời giờ làm việc, rời nơi làm việc/văn phòng trước khi hết giờ làm việc, không thực hiện đúng thời gian làm việc theo lịch đã được phân công', 
    Thời giờ làm việc 44 giờ/tuần: 08giờ/ngày từ thứ 2 đến thứ 6 và buổi sáng thứ 7. Người Lao Động được nghỉ các ngày thứ 7 trong tháng phụ thuộc vào việc sắp xếp công việc từng Phòng ban, Đội nhóm. Buổi sáng: từ 08 giờ đến 12 giờ. Buổi chiều: từ 13 giờ 30 đến 17 giờ 30. Thời giờ làm việc 48 giờ/tuần: 08 giờ/ngày từ thứ 2 đến thứ 7. Buổi sáng: từ 08 giờ đến 12 giờ. Buổi chiều: từ 13 giờ 30 đến 17 giờ 30', 
    . Bố hoặc mẹ hoặc anh, chị, em ruột kết hôn. Ngoài các ngày nghỉ được đề cập tại khoản a, b điều này, Người Lao Động có phát sinh nghỉ khác phải thỏa thuận với Công ty để nghỉ không hưởng lương. Những ngày nghỉ việc riêng phải được sử dụng tại thời điểm xảy ra sự kiện và không được chuyển đổi thành ngày nghỉ bù hoặc thành tiền',
"""

# get a chat completion from the formatted messages
response = chat(chat_prompt.format_prompt(
    user_question="Thời gian làm việc ITL",
    relevant_info=relevant_info
).to_messages())

x=chat_prompt.format_prompt(
    user_question="Thời gian làm việc ITL",
    relevant_info=relevant_info)

x.__dir__()
print(x.messages[1].content)





response=chat("""
You are an expert about policies of ITL Corporation, I will ask you a question, and then provide you some chunks of text contain relevant information. 
Try to extract information from the provided text & answer in Vietnamese. 
You should answer straight to the point of the question, ignore irrelevant information, prefer bullet-points. 
If the text does not contain relevant information, you should tell me that you don't have the answer.

Questions:
Thời gian làm việc ITL  
Relevant Information:

    .1 hoặc một số hành vi dưới đây: Không đúng giờ trong công việc, các buổi họp kinh doanh và/hoặc các khóa tập huấn mà không có lý do chính đáng; Không thông báo trong thời gian sớm nhất có thể được cho người quản lý trực tiếp của mình hoặc người được người quản lý trực tiếp ủy quyền khi Người Lao Động vắng mặt do bị ốm đau hoặc tai nạn hoặc vì bất kỳ lý do nào khác; Làm việc ít giờ hơn khi chưa được phép, cắt ngắn thời giờ làm việc, rời nơi làm việc/văn phòng trước khi hết giờ làm việc, không thực hiện đúng thời gian làm việc theo lịch đã được phân công', 
    Thời giờ làm việc 44 giờ/tuần: 08giờ/ngày từ thứ 2 đến thứ 6 và buổi sáng thứ 7. Người Lao Động được nghỉ các ngày thứ 7 trong tháng phụ thuộc vào việc sắp xếp công việc từng Phòng ban, Đội nhóm. Buổi sáng: từ 08 giờ đến 12 giờ. Buổi chiều: từ 13 giờ 30 đến 17 giờ 30. Thời giờ làm việc 48 giờ/tuần: 08 giờ/ngày từ thứ 2 đến thứ 7. Buổi sáng: từ 08 giờ đến 12 giờ. Buổi chiều: từ 13 giờ 30 đến 17 giờ 30', 
    . Bố hoặc mẹ hoặc anh, chị, em ruột kết hôn. Ngoài các ngày nghỉ được đề cập tại khoản a, b điều này, Người Lao Động có phát sinh nghỉ khác phải thỏa thuận với Công ty để nghỉ không hưởng lương. Những ngày nghỉ việc riêng phải được sử dụng tại thời điểm xảy ra sự kiện và không được chuyển đổi thành ngày nghỉ bù hoặc thành tiền', 

""")

chat?
print('Thời gian làm việc ITL:\n\n- Thời gian làm việc là 44 giờ/tuần hoặc 48 giờ/tuần.\n- Thời gian làm việc từ thứ 2 đến thứ 6 và buổi sáng thứ 7.\n- Buổi sáng: từ 08 giờ đến 12 giờ.\n- Buổi chiều: từ 13 giờ 30 đến 17 giờ 30.\n- Người lao động được nghỉ các ngày thứ 7 trong tháng phụ thuộc vào việc sắp xếp công việc từng phòng ban, đội nhóm.\n- Ngoài các ngày nghỉ được đề cập, người lao động có thể có các ngày nghỉ khác phải thỏa thuận với công ty để nghỉ không hưởng lương.')




## option 2
user_question="Thời gian làm việc của nhân viên ITL?"

prompt=PromptTemplate(
    template = """
You are an expert about policies of ITL Corporation, I will ask you a question, and then provide you some chunks of text contain relevant information. 
Try to extract information from the provided text & answer in Vietnamese. 
You should answer straight to the point of the question, ignore irrelevant information, prefer bullet-points. 
If the text does not contain relevant information, you should tell me that you don't have the answer.

Questions:
{user_question}  

Relevant Information:
{relevant_info}
"""
    ,input_variables=["Thời gian làm việc của nhân viên ITL?", 
                      """.1 hoặc một số hành vi dưới đây: Không đúng giờ trong công việc, các buổi họp kinh doanh và/hoặc các khóa tập huấn mà không có lý do chính đáng; Không thông báo trong thời gian sớm nhất có thể được cho người quản lý trực tiếp của mình hoặc người được người quản lý trực tiếp ủy quyền khi Người Lao Động vắng mặt do bị ốm đau hoặc tai nạn hoặc vì bất kỳ lý do nào khác; Làm việc ít giờ hơn khi chưa được phép, cắt ngắn thời giờ làm việc, rời nơi làm việc/văn phòng trước khi hết giờ làm việc, không thực hiện đúng thời gian làm việc theo lịch đã được phân công', 
    Thời giờ làm việc 44 giờ/tuần: 08giờ/ngày từ thứ 2 đến thứ 6 và buổi sáng thứ 7. Người Lao Động được nghỉ các ngày thứ 7 trong tháng phụ thuộc vào việc sắp xếp công việc từng Phòng ban, Đội nhóm. Buổi sáng: từ 08 giờ đến 12 giờ. Buổi chiều: từ 13 giờ 30 đến 17 giờ 30. Thời giờ làm việc 48 giờ/tuần: 08 giờ/ngày từ thứ 2 đến thứ 7. Buổi sáng: từ 08 giờ đến 12 giờ. Buổi chiều: từ 13 giờ 30 đến 17 giờ 30', 
    . Bố hoặc mẹ hoặc anh, chị, em ruột kết hôn. Ngoài các ngày nghỉ được đề cập tại khoản a, b điều này, Người Lao Động có phát sinh nghỉ khác phải thỏa thuận với Công ty để nghỉ không hưởng lương. Những ngày nghỉ việc riêng phải được sử dụng tại thời điểm xảy ra sự kiện và không được chuyển đổi thành ngày nghỉ bù hoặc thành tiền', 
"""],
)
system_message_prompt = SystemMessagePromptTemplate(prompt=prompt)

prompt=PromptTemplate(
    template="You are a helpful assistant that translates {input_language} to {output_language}.",
    input_variables=["input_language", "output_language"],
)
system_message_prompt = SystemMessagePromptTemplate(prompt=prompt)