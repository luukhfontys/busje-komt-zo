import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from Functions import format_check_omloop
from Gantt_chart import Gantt_chart

# df_planning = pd.read_excel('omloop planning.xlsx')
# fig = Gantt_chart(df_planning)
# fig.show()
st.title('Excel invoer')

if st.button('Test'):
    st.write('Test2')

st_omloop = st.file_uploader('Upload omloop planning', type=['xlsx'])

if st_omloop is not None:
    df_omloop = pd.read_excel(st_omloop)
    format_check = format_check_omloop(df_omloop)
    if all(format_check[:2]):
        st.write(st_omloop.name)
        st.dataframe(df_omloop)
        st.plotly_chart(Gantt_chart(df_omloop))
        st.write('Editable dataframe:')
        st.data_editor(df_omloop, num_rows='dynamic')
    else:
        st.error(f"Error: Your data does not meet the required format.")
        if not format_check[0]:
            st.error("Headers are not in format: [index, 'startlocatie', 'eindlocatie', 'starttijd','eindtijd','activiteit', 'buslijn', 'energieverbruik', 'starttijd datum','eindtijd datum', 'omloop nummer']")
        if not format_check[1]:
            st.error(f'The following (row, colum) data points are not of the right type: {format_check[2]}')
