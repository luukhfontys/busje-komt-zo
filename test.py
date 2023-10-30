from Planning_class import lege_bus
import Planning_functies
import pandas as pd
df = pd.read_excel('Connexxion data - 2023-2024.xlsx')


x = lege_bus(batterij=100.0, omloopnummer=1)

for index in df.index:
    start_locatie = df.loc[index, 'startlocatie']
    eind_locatie = df.loc[index, 'eindlocatie']
    vertrek_tijd = df.loc[index, 'vertrektijd']
    buslijn = df.loc[index, 'buslijn']
    eindtijd = 3
    x.toevoegen_rit(starttijd=vertrek_tijd, start_locatie= start_locatie, eind_locatie= eind_locatie,)
    x
x.controleer_verbruik()