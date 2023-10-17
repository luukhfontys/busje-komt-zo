import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import base64
import matplotlib.pyplot as plt
from bus_class import *
from Functions import *
from Gantt_chart import Gantt_chart
from Functie_to_class_format import *
import plotly.express as px

st.set_page_config(
    page_title='Bussie comes soon',
    layout="wide",
    page_icon="🚌",
    initial_sidebar_state="expanded",
)

# Start pagina en session_state variabelen initializen
if 'page' not in st.session_state:
    st.session_state['page'] = 'Upload and validate'
    st.session_state['df_omloop'] = None
    st.session_state['format_check'] = None
    st.session_state['onderbouwingen'] = None
    st.session_state['batterij_slider'] = None

# Function for the "Upload and Validate" page
def upload_validate_page():
    st.title('Excel invoer')
    st_omloop = st.file_uploader('Upload omloop planning', type=['xlsx'])
    batterij_waarde_slider = st.slider('Selecteer een start waarde voor de batterij', 255, 285, 270)
    st.session_state['batterij_slider'] = batterij_waarde_slider

    if st_omloop is not None:
        df_omloop = pd.read_excel(st_omloop, index_col=0)
        format_check = format_check_omloop(df_omloop)

        if all(format_check[:2]):
            bussen = to_class(df=df_omloop, batterij_waarde=(batterij_waarde_slider, batterij_waarde_slider * 0.1))
            onderbouwingen = return_invalid_busses(bussen)
            st.session_state['onderbouwingen'] = onderbouwingen
            st.success('Data upload successful, proceed to the next page.')
            

            if st.button('Next'):
                st.session_state['df_omloop'] = df_omloop
                st.session_state['format_check'] = format_check
                st.session_state['page'] = 'Overview'



        else:
            st.error(f"Error: Your data does not meet the required format.")
            if not format_check[0]:
                st.error("Headers are not in format: [index, 'startlocatie', 'eindlocatie', 'starttijd', 'eindtijd', 'activiteit', 'buslijn', 'energieverbruik', 'starttijd datum', 'eindtijd datum', 'omloop nummer']")
            if not format_check[1]:
                st.error(f'The following (row, colum) data points are not of the right type: {format_check[2]} \n For cell errors: see marked dataframe below: ')
                st.dataframe(format_check[3])

    


def Overview():
    def cs_sidebar_overview():
        st.sidebar.markdown('---')    
        st.sidebar.markdown("## Overview", unsafe_allow_html=True)
        st.sidebar.markdown(
            "<small>Used for clear insights into the current bus schedule. By switching through pages, more detailed information will be available.</small>",
            unsafe_allow_html=True
        )
        st.sidebar.markdown(
            "<small>If a different bus planning is desired, use 'Import New Excel' option in the menu.</small>",
            unsafe_allow_html=True
        )
        
        st.sidebar.markdown('<small>Explore our [User Manual](https://hubble.cafe/) for step-by-step guidance on using this tool.</small>', unsafe_allow_html=True)
        
        st.sidebar.markdown('---')


        return

    def cs_body_overview():
        col1,col2  = st.columns([1,1])
        score = ['Fail','Unsatisfactory', 'Sufficient', 'Good', 'Excellent']
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
            error_count = 0
            #col2.write('Editable dataframe:')
            #col2.data_editor(df_omloop, num_rows='dynamic')
            for error_message in onderbouwingen:
                error_count += 1             
        else:
            col2.error(f'Data is in the wrong format, please go back to the first page and try again.')
            
    
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
        if error_count >= 3:
            score_planning = score[0]
        elif error_count < 2:
            score_planning = score[1]
        if error_count == 0:
            col1.title('The busplanning passes!')
            col1.header(f"The score of the planning is: {score_planning}")
            col1.subheader(f"")
        else:
            col1.title(f"The busplanning does not pass!")
            col1.header(f"The score of the planning is: {score_planning}")
            col1.subheader('Errors in planning:')
            for error_message in onderbouwingen:
                col1.error(error_message)

    cs_sidebar_overview()
    cs_body_overview()

    return None

def Bus_Specific_Scedule():
    st.title(f"Bus Specific Scedule")
    container = st.container()
    col1, col2 = container.columns([2,1])

      ###
### COLUMN 1 ###
      ###
    totale_bussen = []
    df_omloop = st.session_state['df_omloop']
    for i in range(1, 1+max(st.session_state['df_omloop']['omloop nummer'])):
        totale_bussen.append(f'Bus line {i}')

    selected_Bus = st.sidebar.selectbox(
        "Select a specific busline",
        (totale_bussen),
        index=0
    )
    index_selected_bus = int(selected_Bus[8:])


    fig = Gantt_chart(df_omloop[df_omloop['omloop nummer'] == index_selected_bus])
    fig.update_layout(yaxis=dict(showticklabels=False, domain=[0.5, 1]), title_text= f'Scedule {selected_Bus}',showlegend=False)

    col1.plotly_chart(fig)
    batterij_waarde_slider = st.session_state['batterij_waarde']
    bussen = to_class(df=df_omloop, batterij_waarde=(batterij_waarde_slider, batterij_waarde_slider * 0.1))
    fig2 = make_plot(bussen[index_selected_bus - 1], False)
    col1.pyplot(fig2)
    


      ###
### COLUMN 2 ###
      ###
    dftijdelijk_for_rounding = prestatiemaat_materiaal_minuten(df_omloop[df_omloop['omloop nummer'] == index_selected_bus])[2]
    col2.table({"Minutes material ride":"%.2f" % dftijdelijk_for_rounding})
    mean_material_minutes = (prestatiemaat_materiaal_minuten(df_omloop)[1])
    dfmean_material_minutes = pd.DataFrame({'Average minutes material ride per busline':[mean_material_minutes]})
    col2.table(dfmean_material_minutes.style.format({'Average minutes material ride per busline':"{:.1f}"}))
    
      ###
###  BODY ###
      ###
    if 'begintijd' not in df_omloop.columns:
        expander = st.expander(label=("For a detailed scedule click here"))
        expander.table((df_omloop[df_omloop['omloop nummer'] == index_selected_bus]))
    else:
        expander = st.expander(label=("For a detailed scedule click here"))
        expander.table((df_omloop[df_omloop['omloop nummer'] == index_selected_bus]).drop(columns=['begintijd', 'lengte']))


def Gantt_Chartbestand():    
    st.markdown(
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
    df_omloop = st.session_state['df_omloop']
    fig = Gantt_chart(df_omloop)
    fig.update_layout(
        width=1200, height=700, legend_x=1, legend_y=1)
    st.plotly_chart(fig)













if st.session_state['page'] == 'Upload and validate' or st.session_state['page'] == 'Import New Excel':
    upload_validate_page()
else:
    
    st.sidebar.title("Navigation")
    selected_page = st.sidebar.selectbox(
        "Select a page",
        ('Overview', 'Import New Excel', "Bus Specific Schedule", "Gantt Chart"),
        index=0
    )

    if selected_page == 'Overview':
        Overview()
    elif selected_page == 'Import New Excel':
        upload_validate_page()
        st.session_state['page'] = selected_page
    elif selected_page == "Bus Specific Schedule":
        Bus_Specific_Scedule()
    elif selected_page == 'Gantt Chart':
        Gantt_Chartbestand()