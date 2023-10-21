import base64
from pathlib import Path
from pdf2image import convert_from_path

import streamlit as st

st.set_page_config(
    page_title='User Manual',    #Titel in browser
    page_icon="📖",                               #Icoontje van pagina
)

st.title('Bussie on its way user manual')

pdf_path = "User Manual generic.pdf"
images = convert_from_path(pdf_path)

for image in images:
    st.image(image, use_column_width=True)