import base64
from pathlib import Path
from pdf2image import convert_from_path

import streamlit as st

st.set_page_config(
    page_title='Bussie comes soon user manual',    #Titel in browser
    page_icon="📖",                               #Icoontje van pagina
)

st.title('Bussie comes soon usermanual')

pdf_path = "Runningdinnerprobleem Vughterpoort 2023 - Conceptueel model (3).pdf"
images = convert_from_path(pdf_path)

for image in images:
    st.image(image, use_column_width=True)