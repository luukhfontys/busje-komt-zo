import pandas as pd
from bus_class import bus
from Functie_to_class_format import to_class_format


df = pd.read_excel('omloop planning.xlsx')

batterij = (100,10)
bussen = []
for omloop in range(1,max(df.loc[:,'omloop nummer'])):
    print(omloop)
    locaties, tijden, activiteiten, buslijnen, energieverbruik = to_class_format(df,omloop)
    bussen.append(bus(tijden=tijden, locaties=locaties,
                        activiteit=activiteiten,buslijn=buslijnen,
                        energieverbruik=energieverbruik, omloopnummer=omloop,
                        batterij=batterij
                        ))