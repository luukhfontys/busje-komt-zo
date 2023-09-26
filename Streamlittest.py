import streamlit as st
import pandas as pd

st.title('Excel invoer')

if st.button('Test'):
    st.write('Test2')

st_omloop = st.file_uploader('Upload omloop planning', type=['xlsx'])
    
if st_omloop is not None:
    st.write(st_omloop.name)
    df_omloop = pd.read_excel(st_omloop)
    st.dataframe(df_omloop)
    
if st_omloop is not None:
    st.write('Editable dataframe:')
    editor = st.data_editor(df_omloop, num_rows='dynamic')