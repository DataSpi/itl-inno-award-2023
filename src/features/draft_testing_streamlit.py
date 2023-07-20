import streamlit as st
import numpy as np
import pandas as pd


# st.title("Hello, I am Spino's first Streamlit Web App")
# st.header('This is header, but I dont know it is header 1 or 2 or 3')
# st.markdown("""
# > I can write what ever I want in this markdown block, & *this is awesome*
#             """)

# map_data = pd.DataFrame(
#     np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
#     columns=['lat', 'lon'])

# st.map(map_data)

# st.text_input("Your name", key="name") # user will put there name here. 
# # You can access the value at any point with: st.session_state.name
# st.text(f'hello {st.session_state.name}')


vn_provinces = pd.read_html('https://www.latlong.net/category/cities-243-15.html')
vn_provinces = vn_provinces[0]
vn_provinces.rename(columns={'Latitude':'lat', 'Longitude':'lon'}, inplace=True)
st.dataframe(vn_provinces)
st.map(vn_provinces[['lat', 'lon']])

