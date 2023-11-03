import pandas as pd

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

print(dienstregeling)