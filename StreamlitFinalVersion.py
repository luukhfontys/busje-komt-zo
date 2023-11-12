## Alle benodigde imports, vanuit eige gemaakte bestanden maar ook uit andere librarys

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

## Basis instellingen voor de streamlit pagina.

st.set_page_config(
    page_title='Bussie comes soon',         #Titel in browser
    layout="wide",                          #Type pagina, deze is breed zodat hij het hele scherm vult
    page_icon="🚌",                         #Icoontje van pagina
    initial_sidebar_state="expanded",       #Zorgen dat het menu gelijk open staat
)

## Streamlit irritaties weghalen. Eerst hadden we bij elke titel een "Link" icoontje staan. Deze functie haalt dat weg.

def verberg_suffe_icoontjes():
            st.markdown("""
    <style>
    /* Hide the link button */
    .stApp a:first-child {
        display: none;
    }
    
    .css-15zrgzn {display: none}
    .css-eczf16 {display: none}
    .css-jn99sy {display: none}
    </style>
    """, unsafe_allow_html=True)

## Start pagina en session_state variabelen beginnen zodat deze tussen pagina's door worden meegenomen.

if 'page' not in st.session_state:
    st.session_state['page'] = 'Upload and validate'    # Begin pagina kiezen
    st.session_state['df_omloop'] = None                # Geimporteerde dataframe onthouden. Dit is het omloop schema.
    st.session_state['df_timetable'] = None             # Geimporteerde dataframe onthouden. Dit is de afstand matrix.
    st.session_state['format_check'] = None             # Format check klaarzetten, word gebruikt bij checken van de formatten.
    st.session_state['onderbouwingen'] = None           # Als bij de importeer fase fouten worden gevonden in de data, neemt deze hem mee naar het overview
    st.session_state['batterij_slider'] = None          # De startwaarde van de batterijen aan de hand van een slider.
    st.session_state['bussen'] = None                   # Klaarzetten van de class bussen zodat deze mee kan op alle pagina's.

## Startpagina van de tool. Deze is als functie zodat als er gewisseld word in het menu, 
## de functie kan worden uitgevoerd en de daadwerkelijk juiste pagina word laten zien aan de gebruiker.

def upload_validate_page():
    verberg_suffe_icoontjes()               # Hier halen we dus die icoontjes mee weg.
    st.title('Input Bus Schedule')          # Titel wat er bovenaan de pagina komt te staan.
    st_omloop = st.file_uploader('Upload circulation planning', type=['xlsx'])  # Hier maken we een knop waar de gebruiker een excel bestand kan invoeren.
    st_timetable = st.file_uploader('Upload timetable', type=['xlsx'])          # Hier maken we een tweede knop waar de gebruiker een excel bestand kan invoeren.
    batterij_waarde_slider = st.slider('Select starting value battery in kW-h', 255, 285, 270)  # Hier maken we de slider voor de begin waarde van de batterij. De uiterste waarde zijn de meegeven data vanuit transdev. 
    st.session_state['batterij_slider'] = batterij_waarde_slider                # De session state van de slider word hier vervangen van None naar de waarde die in de slider is meegegeven.

    ## We gaan hier de excel bestanden omschrijven naar dataframes. 
    ## Hier wordt ook gecontroleerd of de opgegeven excelbestanden voldoen aan de vereiste formatten.

    if st_omloop is not None:       # Kijken of er een bestand is opgegeven.
        df_omloop = pd.read_excel(st_omloop, index_col=0)   # Omschrijven naar een dataframe.
        format_check = format_check_omloop(df_omloop)       # Controleren of het format klopt. Dit is een functie uit Functions.py

        if all(format_check[0:2]):           # Hier word gekeken of de output van format_check_omloop klopt.
            error_format_omloop = False     # Dit klopt. Dus zijn er geen errors gevonden.
            df_omloop = drop_tijdloze_activiteit(df_omloop)     # Hier halen we alle activiteiten met een duur van 0 minuten uit de dataset.
            bussen = to_class(df=df_omloop, batterij_waarde=(batterij_waarde_slider, batterij_waarde_slider * 0.1))     # Hier roepen de class bussen aan.
            onderbouwingen = return_invalid_busses(bussen)          # Hier controleren we of er bussen zijn die fouten maken.
            st.session_state['onderbouwingen'] = onderbouwingen     # Hier word de session state vervangen van None naar deze fouten zodat ze kunnen worden meegenomen naar de overview pagina.
            st.success('Data upload successful.')                   # Melding in het groen dat de data succesvol is ontvangen.
            dubbelecheck = 12                                       # Dit is een check om te kijken of de data goed is ontvangen. Komt later weer aanpas.

        else: 
            error_format_omloop = True          # Er zitten fouten in de dataset.
            st.error(f"Error: Your data does not meet the required format.")    # Foutmelding dat de ingevoerde data fouttief is. 
            if not format_check[0]: # Hier controleren we wat de foutmelding is
                st.error("Headers are not in format: [index, 'startlocatie', 'eindlocatie', 'starttijd', 'eindtijd', 'activiteit', 'buslijn', 'energieverbruik', 'starttijd datum', 'eindtijd datum', 'omloop nummer']")
            if not format_check[1]:
                st.error(f'The following (row, colum) data points are not of the right type: {format_check[2]} \n For cell errors: see marked dataframe below: ')
                st.dataframe(format_check[3])
        
        #Dienstregeling upload en dergelijke
        if st_timetable is not None:
            df_dienstregeling = pd.read_excel(st_timetable)
            format_check_afstandm = [True, True]
            format_check_timetb = format_check_timetable(df_dienstregeling)
            try:
                df_afstandsmatrix = pd.read_excel(st_timetable, sheet_name='Afstand matrix')
                format_check_afstandm = format_check_afstandmatrix(df_afstandsmatrix)
                read_success_afstandsmatrix = True
                
            except Exception as e:
                print(e)
                df_afstandsmatrix = None
                read_success_afstandsmatrix = False
                
            if all(format_check_timetb[0:2]) and read_success_afstandsmatrix and all(format_check_afstandm[0:2]):
                checkdr = check_dienstregeling(df_dienstregeling, df_omloop)
                compleet = checkdr[0]
                reden = checkdr[1]
                
                if compleet == True:
                    energieverbruikrows = energieverbruik_check(df_omloop, df_afstandsmatrix)
                    
                    if len(energieverbruikrows) == 0:
                        st.success("Timetable is correct and in the right format, proceed to next page.")
                        if dubbelecheck == 12:
                            if st.button('Next'):
                                st.session_state['df_omloop'] = df_omloop
                                st.session_state['format_check'] = format_check
                                st.session_state['page'] = 'Overview'
                                st.session_state['bussen'] = bussen
                                st.rerun()
                    else:
                        df_energieverbruik_errors = df_omloop.style.apply(highlight_warning_rows, rows=energieverbruikrows, axis=1)
                        warning1 = st.warning("Timetable is correct, but abnormal energy usage by busses detected, see marked dataframe below: ")
                        dataframe = st.dataframe(df_energieverbruik_errors)
                        warning2 = st.warning("This warning can be ignored, or the abnormal energy values can be normalised in the dataset.")
                        if not error_format_omloop:
                            if st.button('Next (Ignore warning)'):
                                st.session_state['df_omloop'] = df_omloop
                                st.session_state['format_check'] = format_check
                                st.session_state['page'] = 'Overview'
                                st.session_state['bussen'] = bussen
                                st.rerun()
                            
                            if st.button('Next (Normalize abnormal values)'):
                                df_omloop = aanpassen_naar_gemiddeld(df_omloop, df_afstandsmatrix, energieverbruikrows)
                                bussen = to_class(df=df_omloop, batterij_waarde=(batterij_waarde_slider, batterij_waarde_slider * 0.1))
                                st.success("Values succesfully normalised, to continue, please press the Next (Normalize abnormal values) button again.")
                                dataframe.empty()
                                warning1.empty()
                                warning2.empty()
                                dataframe = st.dataframe(df_omloop.style.apply(highlight_warning_rows_green, rows=energieverbruikrows, axis=1))
                                st.session_state['df_omloop'] = df_omloop
                                st.session_state['format_check'] = format_check
                                st.session_state['page'] = 'Overview'
                                st.session_state['bussen'] = bussen
                else:
                    st.error(f'Timetable check failed: {reden}')
                    
            else:
                st.error(f"Error: Your timetable does not meet the required format.")
                if not format_check_timetb[0]:
                    st.error("Headers are not in format: ['startlocatie', 'vertrektijd', 'eindlocatie', 'buslijn']")
                if not format_check_timetb[1]:
                    st.error(f'The following (row, colum) data points are not of the right type: {format_check_timetb[2]} \n For cell errors: see marked dataframe below: ')
                    st.dataframe(format_check_timetb[3])
                if read_success_afstandsmatrix == True:
                    if not format_check_afstandm[0]:
                        st.error("Headers of distance matrix are not in format: ['startlocatie', 'eindlocatie', 'min reistijd in min', 'max reistijd in min', 'afstand in meters', 'buslijn']")
                    if not format_check_afstandm[1]:
                        st.error(f'The following (row, colum) data points of the distance matrix are not of the right type: {format_check_afstandm[2]} \n For cell errors: see marked dataframe below: ')
                        st.dataframe(format_check_afstandm[3])
                if read_success_afstandsmatrix == False:
                    st.error("Distance matrix sheet missing in timetable")

                
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
        st.sidebar.markdown("<small>Explore the [user manual](https://bussie-on-its-way-usermanual.streamlit.app/) for step-by-step guidance on using this tool.</small>", unsafe_allow_html=True)
        st.sidebar.markdown('---')

        
        return

    def cs_body_overview():
        col1,col2  = st.columns([1,1])
        score = ['Fail','Unsatisfactory', 'Sufficient', 'Good', 'Excellent']
        #######################################
        # COLUMN 2
        #######################################

        # Display interactive widgets

        
        col2.title('Visualisation')
        onderbouwingen = st.session_state['onderbouwingen']
        df_omloop = st.session_state['df_omloop']
        format_check = st.session_state['format_check']
        
        if all(format_check[0:2]):
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
        
        if error_count >= 3:
            score_planning = score[0]
        elif error_count < 2:
            score_planning = score[1]
        if error_count == 0:
            bussen = st.session_state['bussen']
            data1, data2, data3 = kpis_optellen(bussen)
            data4 = efficientie_maar_dan_gemiddeld(bussen)

            data = {'Performance indicator': ['Total idle time','Total material ride','Total time effective driving', 'Average efficiency'],
                    'Value': [f'{"%.2f" % data1} minutes',f' {"%.2f" % data2} minutes',f'{"%.2f" %  data3} minutes',"%.3f" %  data4 ]}
            col1.title('The busplanning :green[passes]!')
            
            if 0 <= data4 <= 0.6:
                col1.header(f"The score of the planning is: :orange[{score[2]}]")
            elif 0.6 < data4 <= 0.8:
                col1.header(f"The score of the planning is: :green[{score[3]}]")
            elif 0.8 < data4 :
                col1.header(f"The score of the planning is: :green[{score[4]}]")    
            col1.subheader(f"The current performance indicators are:")    
            col1.table(data)

        else:
            col1.title(f"The busplanning does :red[not pass]!")
            col1.header(f"The score of the planning is: :red[{score_planning}]")
            col1.subheader('Errors in planning:')
            for error_message in onderbouwingen:
                col1.error(error_message)

        expander = col1.expander(label=("Tips on improving schedule"))
        expander.markdown(
    """
    There are five grades for planning:
    - :red[Fail]
    - :red[Unsatisfactory]
    - :orange[Sufficient]
    - :green[Good]
    - :green[Excellent] 

    When aiming to enhance the planning from an unsatisfactory level, the focus should be on rectifying errors. \n
    If the planning is sufficient or better, efforts should be directed towards improving performance indicators. This can be accomplished by:
    - Reducing idle time
    - Reducing material ride times
    - Increasing the total minutes of effective driving.
    - Improving average efficiency.
    """
)
    cs_sidebar_overview()
    cs_body_overview()

    return None
def Bus_Specific_Schedule():
    verberg_suffe_icoontjes()
    st.title(f"Bus Specific Schedule")
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
        "Select a specific bus line",
        (totale_bussen),
        index=0
    )
    index_selected_bus = int(selected_Bus[8:])


    fig = Gantt_chart(df_omloop[df_omloop['omloop nummer'] == index_selected_bus])
    fig.update_layout(yaxis=dict(showticklabels=False), title_text= f'Schedule {selected_Bus}',showlegend=False, height=350, width=1150)

    col1.plotly_chart(fig)
    bussen = st.session_state['bussen']
    fig2 = make_plot(bussen[index_selected_bus - 1], False)
    col1.pyplot(fig2, transparent=True)
    
      ###
### COLUMN 2 ###
      ###   

    data = {'Total idle time':f'{"%.2f" % bussen[index_selected_bus-1].idle_minuten} minutes',
            'Total material ride time':f'{ "%.2f" % bussen[index_selected_bus-1].materiaal_minuten} minutes',
            'Total time of effective driving':f'{"%.2f" % bussen[index_selected_bus-1].busminuten} minutes',
            'Number of effective drives':f'{ bussen[index_selected_bus-1].ritten}',
            'Lowest amount of battery':f'{"%.3f" % bussen[index_selected_bus-1].min_lading} kW-h',
            'Final amount of battery' :f'{"%.3f" % bussen[index_selected_bus-1].eind_lading} kW-h',
            'Total time used':f'{"%.2f" % bussen[index_selected_bus-1].totaal} minutes',
            "Total efficiency":f'{"%.3f" % bussen[index_selected_bus-1].efficientie}'}

    for i in range(20): col2.write(" ")  
    col2.table(data)
      ###
###  BODY ###
      ###
    if 'begintijd' not in df_omloop.columns:
        expander = st.expander(label=("For a detailed schedule click here"))
        expander.table((df_omloop[df_omloop['omloop nummer'] == index_selected_bus]))
    else:
        expander = st.expander(label=("For a detailed schedule click here"))
        expander.table((df_omloop[df_omloop['omloop nummer'] == index_selected_bus]).drop(columns=['begintijd', 'lengte']))


def Gantt_Chartbestand():    
    verberg_suffe_icoontjes()
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
        ('Overview', "Bus Specific Schedule", "Gantt Chart",'Import New Excel'),
        index=0
    )

    if selected_page == 'Overview':
        Overview()
    elif selected_page == 'Import New Excel':
        upload_validate_page()
        st.session_state['page'] = selected_page
        st.rerun()
    elif selected_page == "Bus Specific Schedule":
        Bus_Specific_Schedule()
    elif selected_page == 'Gantt Chart':
        Gantt_Chartbestand()