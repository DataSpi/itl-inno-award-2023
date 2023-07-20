import streamlit as st

st.title("Hello, I am Spino's first Streamlit Web App")
st.header('This is header, but I dont know it is header 1 or 2 or 3')
st.markdown("""
> I can write what ever I want in this markdown block, & *this is awesome*
            """)


import numpy as np
import pandas as pd

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(map_data)

st.text_input("Your name", key="name") # user will put there name here. 
# You can access the value at any point with: st.session_state.name
st.text(f'hello {st.session_state.name}')