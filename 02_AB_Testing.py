import streamlit as st
from PIL import Image

st.title("超高性能人工知能なかむら君2号: AB Testing")
st.write("人工知能のなかむら君がABテストの結果を検定してくれます")

# image
image = Image.open('./nakamura/images/c3po.jpeg')
st.image(image, caption='なかむら君',use_column_width=True)
