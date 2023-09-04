import streamlit as st
import numpy as np
import pandas as pd



# st.title("Hello, I am Spino's first Streamlit Web App")
# st.divider()

# if st.button('Say hello'):
#     st.write('Why hello there')
# else:
#     st.write('Goodbye')

# st.divider()
# st.header('This is header, but I dont know it is header 1 or 2 or 3')
# st.markdown("""
# Now, I'll try to draw some geographical plotting over here. Tbh, I am still pretty bad at this, but I believe, I'll get better soon. 
# > the question now is, how can I build a chatbot using streamlit & langchain? 
#             """)


# # st.text_input("Your name", key="name") # user will put there name here. 
# # # You can access the value at any point with: st.session_state.name
# # st.text(f'hello {st.session_state.name}')


# # This is how you plot a map (basic)
# vn_provinces = pd.read_html('https://www.latlong.net/category/cities-243-15.html')
# vn_provinces = vn_provinces[0]
# vn_provinces.rename(columns={'Latitude':'lat', 'Longitude':'lon'}, inplace=True)
# st.dataframe(vn_provinces)
# st.map(vn_provinces[['lat', 'lon']])

# ############
# st.divider()
# genre = st.radio(
#     "What\'s your favorite movie genre",
#     ('Comedy', 'Drama', 'Documentary'))

# if genre == 'Comedy':
#     st.write('You selected comedy.')
# else:
#     st.write("You didn\'t select comedy.")

# ========================================================================================
# oke, now let' get serious & start to build a chatbot
# st.title("Let's try to build a ChatGPT clone")

# with st.chat_message('assistant'):
#     st.write("Hello 🙋‍♂️, I am Spyno's first chatbot")
#     st.bar_chart(np.random.randn(30, 3))

# promt = st.chat_input("let's chat something")
# if promt: 
#     st.write(f"so if you say '{promt}' or what ever, I will always repeat like this. because I do not know anything. I'm just a stupid piece of software at the moment. But I'll improve, right? Do you believe me?")


# ========================================================================================

st.title("This is Echo Bot")
st.write(
"""
**Spyno's note:**
> This is an Echo Bot, I can not do anything else rather than repeating the text that user put in
""")
st.divider()
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
# React to user input
if prompt := st.chat_input("What is up?"): # the `:=` sign is to defining variable & to check if it's not none in just 1 line of code
    # Display user message in chat message container
    with st.chat_message(name="user", avatar="👻"):
        st.markdown(f"User: {prompt}")
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": f"User: {prompt}"})
    
    response = f"Echo: {prompt}"
    # Display assistant response in chat message container
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})