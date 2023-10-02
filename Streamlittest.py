import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from bus_class import bus
from Functions import format_check_omloop
from Gantt_chart import Gantt_chart
from Functie_to_class_format import to_class, return_invalid_busses

st.set_page_config(
    page_title='Busje komt zo',
    page_icon="🚌",
    menu_items={'About': 'https://github.com/luukhfontys/busje-komt-zo'}
)

#Start pagina en session_state variabelen initializen
if 'page' not in st.session_state:
    st.session_state['page'] = 'Upload and validate'
    st.session_state['df_omloop'] = None
    st.session_state['format_check'] = None
    st.session_state['onderbouwingen'] = None

def upload_validate_page():
    st.title('Excel invoer')
    st_omloop = st.file_uploader('Upload omloop planning', type=['xlsx'])

    if st_omloop is not None:
        df_omloop = pd.read_excel(st_omloop)

        bussen = to_class(df=df_omloop)
        onderbouwingen = return_invalid_busses(bussen)
        format_check = format_check_omloop(df_omloop)
        st.session_state['onderbouwingen'] = onderbouwingen

        if all(format_check[:2]):
            
            st.success('Data upload successful, proceed to the next page.')
            st.write(st_omloop.name)
            st.dataframe(df_omloop, height=200)
            
            if st.button('Next'):
                st.session_state['df_omloop'] = df_omloop
                st.session_state['format_check'] = format_check
                st.session_state['page'] = 'Charts'
            
        else:
            st.error(f"Error: Your data does not meet the required format.")
            if not format_check[0]:
                st.error("Headers are not in format: [index, 'startlocatie', 'eindlocatie', 'starttijd','eindtijd','activiteit', 'buslijn', 'energieverbruik', 'starttijd datum','eindtijd datum', 'omloop nummer']")
            if not format_check[1]:
                st.error(f'The following (row, colum) data points are not of the right type: {format_check[2]}')

def charts_page():
    st.title('Grafieken')
    onderbouwingen = st.session_state['onderbouwingen']
    df_omloop = st.session_state['df_omloop']
    format_check = st.session_state['format_check']
    
    if all(format_check[:2]):
            st.plotly_chart(Gantt_chart(df_omloop))
            st.write('Editable dataframe:')
            st.data_editor(df_omloop, num_rows='dynamic')
            
            for error_message in onderbouwingen:
                st.error(error_message)
            
            if st.button('Go back'):
                st.session_state['page'] = 'Upload and validate'
    else:
        st.error(f'Data is in the wrong format, please go back to the first page and try again.')
        
        if st.button('Go back'):
            st.session_state['page'] = 'Upload and validate'


#Pagina wissels:
if st.session_state['page'] == 'Upload and validate':
    upload_validate_page()
elif st.session_state['page'] == 'Charts':
    charts_page()