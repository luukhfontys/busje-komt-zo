import streamlit as st
import pandas as pd
from Gantt_chart import Gantt_chart
import matplotlib.pyplot as plt
import plotly.express as px


# df_planning = pd.read_excel('omloop planning.xlsx')
# fig = Gantt_chart(df_planning)
# fig.show()
st.title('Excel invoer')

if st.button('Test'):
    st.write('Test2')

st_omloop = st.file_uploader('Upload omloop planning', type=['xlsx'])
    
if st_omloop is not None:
    st.write(st_omloop.name)
    df_omloop = pd.read_excel(st_omloop)
    st.dataframe(df_omloop)
    st.plotly_chart(Gantt_chart(df_omloop))
    
if st_omloop is not None:
    st.write('Editable dataframe:')
    editor = st.data_editor(df_omloop, num_rows='dynamic')

