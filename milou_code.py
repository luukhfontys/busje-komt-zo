import pandas as pd
from Klas_deel_twee import scheduled_bus

dienstregeling = pd.read_excel('Connexxion data - 2023-2024.xlsx', sheet_name = 'Dienstregeling')
afstand = pd.read_excel('Connexxion data - 2023-2024.xlsx', sheet_name = 'Afstand matrix')

tijden = []

for index, row in dienstregeling.iterrows():
    tijd = row['vertrektijd']
    x = tijd.split(":")
    uren = int(x[0])
    minuten = int(x[1])
    if uren < 2:
        huidige_tijd = uren * 60 + 24 * 60 + minuten 
    else:
        huidige_tijd = uren * 60 + minuten 
    tijden.append(huidige_tijd)

dienstregeling['huidige tijd'] = tijden


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
bussen = []
for row in dienstregeling.index:
    solved = False
    start_locatie = dienstregeling.loc[row, 'startlocatie']
    vertrektijd = dienstregeling.loc[row, 'huidige tijd']
    buslijn = dienstregeling.loc[row, 'buslijn']
    eind_locatie = dienstregeling.loc[row, 'eindlocatie']
    #while not solved:
    for bus in bussen:    
        solved = bus.add_drive(Time=vertrektijd, First_location=start_locatie, Final_location= eind_locatie, Busline= buslijn)
        if solved:
            break
    if not solved:
        nieuwe_bus = scheduled_bus(afstand, 270.0)
        bussen.append(nieuwe_bus)
        solved = nieuwe_bus.add_drive(Time=vertrektijd, First_location=start_locatie, Final_location= eind_locatie, Busline= buslijn)
print(afstand)
print(bussen[3].schedule)
print(len(bussen))

index = 0
index_lijst = []
startlocatie_lijst = []
eindlocatie_lijst = []
buslijnen = []
begintijden = []
for bus in bussen:
    rooster = bus.schedule
    for key, value in rooster.items():
        index_lijst.append(index)
        index += 1
        startlocatie_lijst.append(value[0])
        eindlocatie_lijst.append(value[1])
        buslijnen.append(value[2])
        begintijden.append(key)

starttijden = []

for i in begintijden:
    minuten = int(i) % 60
    minuten = int(minuten)
    uren = (int(i)- minuten)/60
    uren = int(uren)
    if uren > 24:
        uren = uren - 24
    if uren < 10:
        uren = f'0{uren}'
    if minuten < 10:
        minuten = f'0{minuten}'
    starttijd = f'{uren}:{minuten}:00'
    starttijden.append(starttijd)

bus_new = []
for i in buslijnen:
    if i == 1.0:
        i = ''
    bus_new.append(i)
    

nieuwe_planning = pd.DataFrame()
nieuwe_planning['startlocatie'] = startlocatie_lijst
nieuwe_planning['eindlocatie'] = eindlocatie_lijst
nieuwe_planning['starttijd'] = starttijden


