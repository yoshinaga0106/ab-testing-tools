import streamlit as st
from PIL import Image

# title
st.title("AB testing tools")
st.write("Calculate sample size / Statistical test (under constructions.)")

# image
image = Image.open('./nakamura/images/ab.jpeg')
st.image(image, use_column_width=True)
