import pandas as pd
from bus_class import bus
from Functie_to_class_format import to_class, return_invalid_busses

df = pd.read_excel('omloop planning.xlsx')

bussen = to_class(df=df,batterij_waarde=(251,10))

return_invalid_busses(bussen)

##### dingen om te doen:
### local vs global
### local
# speling (handing om te weten per bus)
# materiaal minuten ( functie maken in class, die aanroepen voor batterij check en voor materiaal)
#
### global
# aantal omlopen
# Dienstregeling
# 
