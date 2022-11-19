import streamlit as st
from PIL import Image

# title
st.title("超高性能人工知能C-3PO")
st.write("人工知能のC-3POがサンプルサイズを計算したりABテストの結果を検定してくれます")

# image
image = Image.open('./nakamura/images/c3po.jpeg')
st.image(image, caption='人工知能',use_column_width=True)
