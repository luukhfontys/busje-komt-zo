import pandas as pd
from bus_class import bus
from Functie_to_class_format import to_class, return_invalid_busses, reverse_sort, check_dienstregeling

df = pd.read_excel('omloop planning.xlsx')
df_dienstregeling = pd.read_excel('Connexxion data - 2023-2024.xlsx', sheet_name='Dienstregeling')

#bussen = to_class(df=df,batterij_waarde=(251,10))

bussen = to_class(df=df)
for i in range(1):
    for bus in bussen:
        print(bus.omloopnummer)
    print('----------')
    print('Line break')
    print('----------')
    bussen.sort()
    for bus in bussen:
        print(bus.omloopnummer)
    print('----------')
    print('Line break')
    print('----------')    
    bussen = reverse_sort(bussen=bussen)
    for bus in bussen:
        print(bus.omloopnummer)
    print('----------')
    print('Line break')
    print('----------')
    onderbouwingen = return_invalid_busses(bussen)

print(check_dienstregeling(df_planning=df, df_dienstregeling=df_dienstregeling))

##### dingen om te doen:
### local vs global
### local
# speling (handing om te weten per bus) # hoe defineren we momenteel speling
# materiaal minuten ( functie maken in class, die aanroepen voor batterij check en voor materiaal) !
#
### global
# aantal omlopen
# Dienstregeling
# 
