import pandas as pd
from Klas_deel_twee import scheduled_bus
import numpy as np

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
iteration = 0
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
        iteration += 1
        nieuwe_bus = scheduled_bus(afstand, 270.0, omloop=iteration)
        bussen.append(nieuwe_bus)
        solved = nieuwe_bus.add_drive(Time=vertrektijd, First_location=start_locatie, Final_location= eind_locatie, Busline= buslijn)
#print(afstand)
#print(bussen[3].schedule)
#print(len(bussen))

index = 0
index_lijst = []
startlocatie_lijst = []
eindlocatie_lijst = []
buslijnen = []
begintijden = []
omlopen = []

for bus in bussen:
    rooster = bus.schedule
    for key, value in rooster.items():
        omlopen.append(bus.omloop)
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

activiteiten = []
buslijn = []
for i in buslijnen:
    if i == 400 or i == 401:
        buslijn.append(i)
        activiteiten.append('dienst rit')
    elif i == 1.0:
        buslijn.append(np.nan)
        activiteiten.append('materiaal rit')
    elif i == 0.0:
        buslijn.append(np.nan)
        activiteiten.append('Opladen')
    else:
        activiteiten.append('idle')
        buslijn.append(np.nan)

datum_vandaag = '06-11-2023'
datum_morgen = '07-11-2023'

nieuwe_planning = pd.DataFrame()
nieuwe_planning['startlocatie'] = startlocatie_lijst
nieuwe_planning['eindlocatie'] = eindlocatie_lijst
nieuwe_planning['starttijd'] = starttijden
nieuwe_planning['activiteit'] = activiteiten
nieuwe_planning['buslijn'] = buslijn

datums = []

for i in begintijden:
    minuten = int(i) % 60
    minuten = int(minuten)
    uren = (int(i)- minuten)/60
    uren = int(uren)
    if uren >= 24:
        uren = uren - 24
        if uren < 10:
            uren= f'0{uren}'
        if minuten < 10:
            minuten = f'0{minuten}'
        dag_morgen = f'{datum_morgen} {uren}:{minuten}:00'
        datums.append(dag_morgen)
    else:
        if uren < 10:
            uren= f'0{uren}'
        if minuten < 10:
            minuten = f'0{minuten}'
        dag_vandaag = f'{datum_vandaag} {uren}:{minuten}:00'
        datums.append(dag_vandaag)

nieuwe_planning['starttijd datum'] = datums
nieuwe_planning['omloop nummer'] = omlopen

print(nieuwe_planning)
verbruik = []

for index, row in nieuwe_planning.iterrows():
    #stap 2
    rit = row['activiteit']
    if rit == 'idle':
        verbruik.append(0.01)
    #stap 3
    elif rit == 'dienst rit':
        correcte_buslijn = afstand[afstand['buslijn'] == row['buslijn']]
        correcte_rit = correcte_buslijn[correcte_buslijn['startlocatie'] == row['startlocatie']]
        verbruik.append(correcte_rit['afstand in meters']/1000 * 1.6)
    elif rit == 'materiaal rit':
        start_locatie = row['startlocatie']
        eind_locatie = row['eindlocatie']
        
        correct_eind = afstand[afstand['eindlocatie'] == eind_locatie]
        correcte_rit = correct_eind[correct_eind['startlocatie'] == start_locatie]
        if start_locatie == 'ehvgar' or eind_locatie == 'ehvgar':
            verbruik.append(correcte_rit['afstand in meters']/1000 * 1.6)
        else:
            afstand_colomn = correcte_rit['afstand in meters']
            laatste_waarde = afstand_colomn.iloc[-1]
            verbruik.append(laatste_waarde/1000 * 1.6)
    elif rit == 'opladen':
        verbruik.append(225.0)
        
        # for line in afstand.index:
        #     first_location = afstand.loc[line, 'startlocatie']
        #     final_location = afstand.loc[line, 'eindlocatie']
        #     busline = afstand.loc[line, 'buslijn']
        #     batterij = afstand.loc[line, 'verbruik']
        #     time = afstand.loc[line, 'max reistijd in min']
            

            
