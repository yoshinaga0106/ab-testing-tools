import streamlit as st
from PIL import Image

st.title("AB Testing")
st.write("Under Construnctions")

# image
image = Image.open('./abtools/images/under_constructions.jpeg')
st.image(image, use_column_width=True)
