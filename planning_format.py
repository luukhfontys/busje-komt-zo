import pandas as pd
from planning_generaliseren import scheduled_bus
import numpy as np


def importeren(bestandsnaam:str='Connexxion data - 2023-2024.xlsx', sheetnaam1:str='Dienstregeling', sheetnaam2:str='Afstand matrix'):
    ''' importeerd de relevante data uit excelsheets
    '''
    dienstregeling = pd.read_excel(bestandsnaam, sheet_name = sheetnaam1)
    afstand = pd.read_excel(bestandsnaam, sheet_name = sheetnaam2)
    return dienstregeling, afstand

def tijden_minuten(dienstregeling):
    '''Zet de vertrektijden om in minuten en voegt deze minuten toe aan het dataframe. Vervolgens worden 
        de minuten gesorteerd van laag naar hoog
        Args: Dienstregeling(DataFrame)
        Return: Dienstregeling(DataFrame)'''
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
    dienstregeling = dienstregeling.sort_values(by=['huidige tijd'])
    return dienstregeling

#Verbruik per kilometer ligt tussen de 0.7 en 2.5 kWh
# verbruik = []
# for index, row in dienstregeling.iterrows():
#     startlocatie = row['startlocatie']
#     eindlocatie = row['eindlocatie']
#     lijn = row['buslijn']
#     for index, row in afstand.iterrows():
#         eindlocatie2 = row['eindlocatie']
#         startlocatie2 = row['startlocatie']
#         lijn2 = row['buslijn']
#         afstand_meter = row['afstand in meters']
#         if startlocatie == startlocatie2 and eindlocatie == eindlocatie2 and lijn == lijn2:
#             afstand_kilometer = afstand_meter / 1000
#             verbruik.append(afstand_kilometer * 1.6)

# dienstregeling['verbruik'] = verbruik
def verbruik_afstands_matrix(afstand:pd.DataFrame)->pd.DataFrame:
    verbruik_afstand = []
    for index, row in afstand.iterrows():
        afstand_meter = row['afstand in meters']
        afstand_kilometer = afstand_meter / 1000
        verbruik_afstand.append(afstand_kilometer * 1.6)
    afstand['verbruik'] = verbruik_afstand
    return afstand

def create_planning(dienstregeling:pd.DataFrame, afstand:pd.DataFrame,batterijwaarde:float=270)->list:
    ''' Maakt een planning op basis van de ingegeven dienstregeling en afstandsmatrix
    volgt pseudo code zoals te vinden in pseudocode.txt
    '''
    bussen = []
    iteration = 0
    for row in dienstregeling.index:
        #print(len(bussen))
        solved = False
        start_locatie = dienstregeling.loc[row, 'startlocatie']
        vertrektijd = dienstregeling.loc[row, 'huidige tijd']
        buslijn = dienstregeling.loc[row, 'buslijn']
        eind_locatie = dienstregeling.loc[row, 'eindlocatie']
        ### updaten locaties
        for bus in bussen:
            bus.location_match(start_locatie)
            #print(bus.correct_location)
        bussen.sort()
        for bus in bussen:    
            solved = bus.add_drive(Time=vertrektijd, First_location=start_locatie, Final_location= eind_locatie, Busline= buslijn)
            if solved:
                break
        if not solved:
            iteration += 1
            nieuwe_bus = scheduled_bus(afstand, batterijwaarde, omloop=iteration)
            bussen.append(nieuwe_bus)
            solved = nieuwe_bus.add_drive(Time=vertrektijd, First_location=start_locatie, Final_location= eind_locatie, Busline= buslijn)
    return bussen

def oplossing_uitlezen(bussen):
    '''Zet de gemaakte oplossing om in lijsten voor het maken van een planning'''
    startlocatie_lijst = []
    eindlocatie_lijst = []
    buslijnen = []
    begintijden = []
    omlopen = []

    for bus in bussen:
        rooster = bus.schedule
        for key, value in rooster.items():
            omlopen.append(bus.omloop)
            startlocatie_lijst.append(value[0])
            eindlocatie_lijst.append(value[1])
            buslijnen.append(value[2])
            begintijden.append(key)

    return startlocatie_lijst, eindlocatie_lijst, buslijnen, begintijden, omlopen 

def starttijden_goedzetten(begintijden, datum_morgen, datum_vandaag):
    '''Zet de lijst met minuten terug in het goede format van uren en minuten
    Args: begintijden(lijst) met tijd in minuten
    Returns: startijden(lijst) met tijd in uren, minuten
    datums(lijst) met datum van starttijd en daarna de uren en minuten'''
    starttijden = []
    for i in begintijden:
        minuten = int(i) % 60
        minuten = int(minuten)
        uren = (int(i)- minuten)/60
        uren = int(uren)
        if uren >= 24:
            uren = uren - 24
        if uren < 10:
            uren = f'0{uren}'
        if minuten < 10:
            minuten = f'0{minuten}'
        starttijd = f'{uren}:{minuten}:00'
        starttijden.append(starttijd)

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

    return starttijden, datums

def activiteit_buslijn(buslijnen):
    '''Kijkt naar wat voor activiteit de bus aan het doen is
    Args: buslijnen(lijst)
    Returns: activiteiten(lijst) met activiteiten van de bus
    buslijn(lijst) met buslijnen'''
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
    return activiteiten

def begin_planning(bussen, afstand, dienstregeling,datum_morgen, datum_vandaag):
    '''Maakt de nieuwe planning aan'''
    startlocatie_lijst, eindlocatie_lijst, buslijn, begintijden, omlopen = oplossing_uitlezen(bussen)
    starttijden, datums = starttijden_goedzetten(begintijden, datum_morgen, datum_vandaag)
    activiteiten = activiteit_buslijn(buslijn)
    nieuwe_planning = pd.DataFrame()
    nieuwe_planning['startlocatie'] = startlocatie_lijst
    nieuwe_planning['eindlocatie'] = eindlocatie_lijst
    nieuwe_planning['starttijd'] = starttijden
    nieuwe_planning['activiteit'] = activiteiten
    nieuwe_planning['buslijn'] = buslijn
    verbruik = verbruik_matrix(nieuwe_planning, afstand)
    duur = lengte_rit(nieuwe_planning, afstand)
    eindtijden, datums_eind = eindtijden_goedzetten(begintijden, duur, datum_morgen, datum_vandaag)
    nieuwe_planning['eindtijd'] = eindtijden
    nieuwe_planning['energieverbruik'] = verbruik
    nieuwe_planning['starttijd datum'] = datums
    nieuwe_planning['eindtijd datum'] = datums_eind
    nieuwe_planning['omloop nummer'] = omlopen

    cols = nieuwe_planning.columns.tolist()
    cols = ['startlocatie', 'eindlocatie', 'starttijd', 'eindtijd', 'activiteit', 'buslijn', 'energieverbruik', 'starttijd datum', 'eindtijd datum', 'omloop nummer']
    df = nieuwe_planning[cols]

    df[['starttijd datum', 'eindtijd datum']] = df[['starttijd datum', 'eindtijd datum']].apply(pd.to_datetime)

    df.to_excel('OmloopplanningIdleop2Min.xlsx')
    return

def verbruik_matrix(nieuwe_planning, afstand):
    '''Kijkt naar alle ritten uit de planning en zoekt uit de afstandsmatrix het juiste verbruik erbij
    Args: nieuwe_planning(DataFrame)
    Return: verbruik(lijst)'''
    verbruik = []

    for index, row in nieuwe_planning.iterrows():
        rit = row['activiteit']
        if rit == 'idle':
            verbruik.append(0.01)
        elif rit == 'dienst rit':
            correcte_buslijn = afstand[afstand['buslijn'] == row['buslijn']]
            correcte_rit = correcte_buslijn[correcte_buslijn['startlocatie'] == row['startlocatie']]
            verbruik.append(int(correcte_rit['afstand in meters'])/1000 * 1.6)
        elif rit == 'materiaal rit':
            start_locatie = row['startlocatie']
            eind_locatie = row['eindlocatie']
        
            correct_eind = afstand[afstand['eindlocatie'] == eind_locatie]
            correcte_rit = correct_eind[correct_eind['startlocatie'] == start_locatie]
            if start_locatie == 'ehvgar' or eind_locatie == 'ehvgar':
                verbruik.append(int(correcte_rit['afstand in meters'])/1000 * 1.6)
            else:
                afstand_colomn = correcte_rit['afstand in meters']
                laatste_waarde = afstand_colomn.iloc[-1]
                verbruik.append(int(laatste_waarde)/1000 * 1.6)
        elif rit == 'Opladen':
            verbruik.append(-225.0/2)
        else:
            ''
            #print('foutcode')
    return verbruik

def lengte_rit(nieuwe_planning, afstand):
    '''Kijkt naar alle ritten uit de planning en zoekt uit de afstandsmatrix het juist aantal minuten erbij
    Args: nieuwe_planning(DataFrame)
    Return: Duur(lijst) met aantal minuten per rit'''
    duur = []

    for index, row in nieuwe_planning.iterrows():
        rit = row['activiteit']
        if rit == 'idle':
            duur.append(1)  
        elif rit == 'dienst rit':
            correcte_buslijn = afstand[afstand['buslijn'] == row['buslijn']]
            correcte_rit = correcte_buslijn[correcte_buslijn['startlocatie'] == row['startlocatie']]
            duur.append(int(correcte_rit['max reistijd in min']))
        elif rit == 'materiaal rit':
            start_locatie = row['startlocatie']
            eind_locatie = row['eindlocatie']
        
            correct_eind = afstand[afstand['eindlocatie'] == eind_locatie]
            correcte_rit = correct_eind[correct_eind['startlocatie'] == start_locatie]
            if start_locatie == 'ehvgar' or eind_locatie == 'ehvgar':
                duur.append(int(correcte_rit['max reistijd in min']))
            else:
                afstand_colomn = correcte_rit['max reistijd in min']
                laatste_waarde = afstand_colomn.iloc[-1]
                duur.append(int(laatste_waarde))
        elif rit == 'Opladen':
            duur.append(15)
        else:
            ' '
            #print('foutcode')
            
    return duur

def eindtijden_goedzetten(begintijden, duur, datum_morgen, datum_vandaag):
    '''Voegt bij de starttijden het aantal met minuten van de rit toe. Zet de lijst met minuten terug 
    in het goede format van uren en minuten
    Args: begintijden(lijst) met tijd in minuten
    duur(lijst) met lengte van de rit
    Returns: eindtijden(lijst) met tijd in uren, minuten
    datums_eind(lijst) met datum van eindtijd en daarna de uren en minuten'''
    begintijden = [int(x) for x in begintijden]
    np_begintijden = np.array(begintijden)
    np_duur = np.array(duur)
    tijd_eind = np_begintijden + np_duur

    eindtijden = []

    for i in tijd_eind:
        minuten = int(i) % 60
        minuten = int(minuten)
        uren = (int(i)- minuten)/60
        uren = int(uren)
        if uren >= 24:
            uren = uren - 24
        if uren < 10:
            uren = f'0{uren}'
        if minuten < 10:
            minuten = f'0{minuten}'
        eindtijd = f'{uren}:{minuten}:00'
        eindtijden.append(eindtijd)

    datums_eind = []
    for i in tijd_eind:
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
            datums_eind.append(dag_morgen)
        else:
            if uren < 10:
                uren= f'0{uren}'
            if minuten < 10:
                minuten = f'0{minuten}'
            dag_vandaag = f'{datum_vandaag} {uren}:{minuten}:00'
            datums_eind.append(dag_vandaag)
    return eindtijden, datums_eind

# def planning_compleet(bussen,afstand, eindtijden, datums_eind):
#     nieuwe_planning, omlopen, datums = begin_planning(bussen)
#     verbruik = verbruik_matrix(nieuwe_planning, afstand)
#     eindtijden_goedzetten()
#     nieuwe_planning['eindtijd'] = eindtijden
#     nieuwe_planning['energieverbruik'] = verbruik
#     nieuwe_planning['starttijd datum'] = datums
#     nieuwe_planning['eindtijd datum'] = datums_eind
#     nieuwe_planning['omloop nummer'] = omlopen

#     cols = nieuwe_planning.columns.tolist()
#     cols = ['startlocatie', 'eindlocatie', 'starttijd', 'eindtijd', 'activiteit', 'buslijn', 'energieverbruik', 'starttijd datum', 'eindtijd datum', 'omloop nummer']
#     df = nieuwe_planning[cols]

#     df[['starttijd datum', 'eindtijd datum']] = df[['starttijd datum', 'eindtijd datum']].apply(pd.to_datetime)

#     df.to_excel('OmloopplanningIdleop2Min.xlsx')

def main():
    datum_vandaag = '11-13-2023'
    datum_morgen = '11-14-2023'
    dienstregeling, afstand = importeren()
    afstand = verbruik_afstands_matrix(afstand=afstand)
    dienstregeling = tijden_minuten(dienstregeling)
    bussen = create_planning(dienstregeling, afstand)
    begin_planning(bussen,afstand,dienstregeling,datum_morgen,datum_vandaag)

if __name__ == '__main__':
    main()
