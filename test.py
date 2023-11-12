# from Planning_class import lege_bus
# import Planning_functies
# import pandas as pd
# df = pd.read_excel('Connexxion data - 2023-2024.xlsx')


# x = lege_bus(batterij=100.0, omloopnummer=1)

# for index in df.index:
#     start_locatie = df.loc[index, 'startlocatie']
#     eind_locatie = df.loc[index, 'eindlocatie']
#     vertrek_tijd = df.loc[index, 'vertrektijd']
#     buslijn = df.loc[index, 'buslijn']
#     eindtijd = 3
#     x.toevoegen_rit(starttijd=vertrek_tijd, start_locatie= start_locatie, eind_locatie= eind_locatie,)
#     x
# x.controleer_verbruik()

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

df_dienstregeling = pd.read_excel('NieuwePlanning.xlsx')

#Verbruik per kilometer ligt tussen de 0.7 en 2.5 kWh
verbruik = []
for index, row in dienstregeling.iterrows():
    startlocatie = row['startlocatie']
    eindlocatie = row['eindlocatie']
    lijn = row['buslijn']
    for index, row in afstand.iterrows():
        eindlocatie2 = row['eindlocatie']
        startlocatie2 = row['startlocatie']
        lijn2 = row['buslijn']
        afstand_meter = row['afstand in meters']
        if startlocatie == startlocatie2 and eindlocatie == eindlocatie2 and lijn == lijn2:
            afstand_kilometer = afstand_meter / 1000
            verbruik.append(afstand_kilometer * 1.6)

dienstregeling['verbruik'] = verbruik

verbruik_afstand = []
for index, row in afstand.iterrows():
    afstand_meter = row['afstand in meters']
    afstand_kilometer = afstand_meter / 1000
    verbruik_afstand.append(afstand_kilometer * 1.6)

afstand['verbruik'] = verbruik_afstand