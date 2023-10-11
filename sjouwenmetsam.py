import streamlit as st
from pathlib import Path
import base64
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from bus_class import bus
from Functions import format_check_omloop
from Gantt_chart import Gantt_chart
from Functie_to_class_format import to_class, return_invalid_busses



st.set_page_config(
     page_title='Bussie comes soon',
     layout="wide",
     page_icon="🚌",
     initial_sidebar_state="expanded",
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
    batterij_waarde_slider = st.slider('Selecteer een start waarde voor de batterij', 255, 285, 270)
    
    if st_omloop is not None:
        df_omloop = pd.read_excel(st_omloop, index_col=0)

        format_check = format_check_omloop(df_omloop)
        

        if all(format_check[:2]):
            
            bussen = to_class(df = df_omloop, batterij_waarde = (batterij_waarde_slider, batterij_waarde_slider*0.1))
            onderbouwingen = return_invalid_busses(bussen)
            st.session_state['onderbouwingen'] = onderbouwingen
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
                st.error("Headers are not in format: [index, 'startlocatie', 'eindlocatie', 'starttijd', 'eindtijd', 'activiteit', 'buslijn', 'energieverbruik', 'starttijd datum', 'eindtijd datum', 'omloop nummer']")
            if not format_check[1]:
                st.error(f'The following (row, colum) data points are not of the right type: {format_check[2]} \n For cell errors: see marked dataframe below: ')
                st.dataframe(format_check[3])



def main():
    cs_sidebar()
    cs_body()

    return None

def cs_sidebar():
    
    st.sidebar.markdown(
    f'''
        <style>
            .sidebar .sidebar-content {{
                width: 375px;
            }}
        </style>
    ''',
    unsafe_allow_html=True)

    st.sidebar.header('Busje On His Way')

    st.sidebar.markdown('Import Excel')

    st.sidebar.markdown('Bus Schedule')

    st.sidebar.markdown('Gantt Chart')

    st.sidebar.markdown('Performance Indicators')

    st.sidebar.markdown('<small>Learn more about [Zuipen in Hubble](https://hubble.cafe/)</small>', unsafe_allow_html=True)

    st.sidebar.markdown('''<hr>''', unsafe_allow_html=True)

    return None

##########################
# Main body of Bussie Komt Zo 
##########################

def cs_body():
    col1,col2  = st.columns([1,1])
    #######################################
    # COLUMN 1
    #######################################    
    col1.markdown(
    """
    <style>
    .main .block-container {
        padding-right: 30px;
        padding-left: 30px;
        padding-top: 30px;
        padding-bottom: 3px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

    col1.title('What The User Snatses will apear here')
    # Display data

    col1.subheader('Display data')
    col1.code('''
Alle eendjes zwemmen in het water
Falderalderiere, falderalderare
Alle eendjes zwemmen in het water
Fal-de, falderaldera
Alle eendjes zwemmen in het water
Falderalderiere, falderalderare
Alle eendjes zwemmen in het water
Fal-de, falderaldera
    ''')

 

    #######################################
    # COLUMN 2
    #######################################

    # Display interactive widgets

    
    col2.title('Grafieken')
    onderbouwingen = st.session_state['onderbouwingen']
    df_omloop = st.session_state['df_omloop']
    format_check = st.session_state['format_check']
    
    if all(format_check[:2]):
        col2.plotly_chart(Gantt_chart(df_omloop))
        #col2.write('Editable dataframe:')
        #col2.data_editor(df_omloop, num_rows='dynamic')
        
        for error_message in onderbouwingen:
            col2.error(error_message)
        
        if col2.button('Go back'):
            col2.session_state['page'] = 'Upload and validate'
    else:
        col2.error(f'Data is in the wrong format, please go back to the first page and try again.')
            
        if col2.button('Go back'):
            col2.session_state['page'] = 'Upload and validate'


#Pagina wissels:
if st.session_state['page'] == 'Upload and validate':
    upload_validate_page()
elif st.session_state['page'] == 'Charts':
    main()