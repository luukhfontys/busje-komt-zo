import pandas as pd
from bus_class import bus
from Functie_to_class_format import to_class


df = pd.read_excel('omloop planning.xlsx')

bussen = to_class(df=df,batterij_waarde=(10000,10))

bussen.sort()

for bus in bussen:
    if bus.valide == 0:
        print(bus.omloopnummer)