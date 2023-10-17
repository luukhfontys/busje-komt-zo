import pandas as pd
from bus_class import bus
import matplotlib.pyplot as plt

def to_class(df:pd.DataFrame, batterij_waarde:tuple[float,float]=(270,27.0)): #hier slider maken voor streamlit
    bussen = []
    for omloop in range(1,max(df.loc[:,'omloop nummer']) + 1):
        locaties, tijden, activiteiten, buslijnen, energieverbruik = to_class_format(df,omloop)
        bussen.append(bus(tijden=tijden,
                          locaties=locaties,
                          activiteit=activiteiten,
                          buslijn=buslijnen,
                          energieverbruik=energieverbruik, 
                          omloopnummer=omloop,
                          batterij=batterij_waarde
                          ))
    return bussen
        
def to_class_format(df:pd.DataFrame, omloop:int):
    df_omloop = df[df['omloop nummer'] == omloop]
    df_omloop.reset_index(drop=True, inplace=True)
    startlocaties = df_omloop.loc[:,'startlocatie']
    eindlocaties = df_omloop.loc[:,'eindlocatie']
    starttijden = df_omloop.loc[:,'starttijd']
    eindtijden = df_omloop.loc[:,'eindtijd']
    activiteit = df_omloop.loc[:,'activiteit']
    buslijn = df_omloop.loc[:,'buslijn']
    energieverbruik_van_rit = df_omloop.loc[:,'energieverbruik']
    
    locaties= []
    tijden = []
    activiteiten = []
    buslijnen = []
    energieverbruik = []
    
    for index in range(len(startlocaties)):
        locaties.append((startlocaties[index], eindlocaties[index]))
        tijden.append((starttijden[index],eindtijden[index]))
        activiteiten.append(activiteit[index])
        buslijnen.append(buslijn[index])
        energieverbruik.append(energieverbruik_van_rit[index])  
        
    return locaties, tijden, activiteiten, buslijnen, energieverbruik

def return_invalid_busses(bussen:list[object]):
    bussen.sort()
    itteration = 0
    done = False
    invalide_bussen = []
    while not done and itteration < len(bussen):
        bus = bussen[itteration]
        itteration +=1
        if bus.valide == 0:
            # hier kunnen we de write output van streamlit gebruiken
            invalide_bussen.append(bus.onderbouwing)
        elif bus.valide == 1:
            done = True 
    
    return invalide_bussen

def reverse_sort(bussen:list[object]):
    for bus in bussen:
        bus.sorteren_op_fouten = False
    bussen.sort()
    return bussen

def check_dienstregeling(df_dienstregeling:pd.DataFrame, df_planning:pd.DataFrame):
    compleet = True
    iteration = 0
    maximum = len(df_dienstregeling.index)
    while compleet and iteration < maximum:
        start_locatie = df_dienstregeling.loc[iteration, 'startlocatie']
        #eind_locatie = df_dienstregeling.loc[iteration, 'eindlocatie']
        buslijn = df_dienstregeling.loc[iteration, 'buslijn']
        tijd = df_dienstregeling.loc[iteration, 'vertrektijd'] + ':00'
        iteration += 1
        df_planning_buslijn = df_planning[df_planning.loc[:,'buslijn'] == buslijn]
        df_planning_start_locatie = df_planning_buslijn[df_planning_buslijn.loc[:,'startlocatie'] == start_locatie]
        df_planning_tijd = df_planning_start_locatie[df_planning_start_locatie.loc[:,'starttijd'] == tijd]
        if len(df_planning_tijd.index) == 0:
            compleet = False
            print('oh jeee')  
    return compleet

def make_plot(bus:object, kleurenblind:bool=False):
    bus.force_calc()
    if kleurenblind:
        kleur1 = 'blue'
        kleur2 = 'orange'
    else:
        kleur1 = 'lime'
        kleur2 = 'red'    
    plt.plot(bus.batterij_geschiedenis, color=kleur1)
    plt.plot([bus.batterijstart[1]]* len(bus.batterij_geschiedenis), color=kleur2)
    return

def drop_tijdloze_activiteit(df:pd.DataFrame):
    indexen_met_tijd_0 = []
    for index in df.index:
        if df.loc[index, 'starttijd'] == df.loc[index, 'eindtijd']:
            #print(df.loc[index, :])
            indexen_met_tijd_0.append(index)
    df.drop(indexen_met_tijd_0, inplace=True)
    return df

def energieverbruik_check(df:pd.DataFrame, df_afstanden:pd.DataFrame):
    indexen_voor_false = []
    ondergrens_verbruik = 0.7
    bovengrens_verbruik = 2.5
    #df['geloofwaardig'] = True # colomn toegoeven
    # idle
    df_idle = df[df['activiteit'] == 'idle']
    df_checked = df_idle[df_idle['energieverbruik'] != 0.01]
    indexen_voor_false += list(df_checked.index)
    # dienstrit ehvapt- ehvbst lijn 400
    afstand_in_km = int(df_afstanden.loc[0, 'afstand in meters']/1000)
    df_400 = df[df['buslijn'] == 400.0]
    df_400_apt = df_400[df_400['startlocatie'] == 'ehvapt']
    #ondergrens
    df_checked = df_400_apt[df_400_apt['energieverbruik'] <= (ondergrens_verbruik * afstand_in_km)]
    indexen_voor_false += list(df_checked.index)
    #bovengrens
    df_checked = df_400_apt[df_400_apt['energieverbruik'] >= (bovengrens_verbruik * afstand_in_km)]
    indexen_voor_false += list(df_checked.index)
    
    # dienstrit ehvbst- ehvapt lijn 400
    afstand_in_km = int(df_afstanden.loc[1, 'afstand in meters']/1000)
    df_400 = df[df['buslijn'] == 400.0]
    df_400_bst = df_400[df_400['startlocatie'] == 'ehvbst']
    #ondergrens
    df_checked = df_400_bst[df_400_bst['energieverbruik'] <= (ondergrens_verbruik * afstand_in_km)]
    indexen_voor_false += list(df_checked.index)
    #bovengrens
    df_checked = df_400_bst[df_400_bst['energieverbruik'] >= (bovengrens_verbruik * afstand_in_km)]
    indexen_voor_false += list(df_checked.index)
        
    # dienstrit ehvapt- ehvbst lijn 401
    afstand_in_km = int(df_afstanden.loc[2, 'afstand in meters']/1000)
    df_401 = df[df['buslijn'] == 401.0]
    df_401_apt = df_401[df_401['startlocatie'] == 'ehvapt']
    #ondergrens
    df_checked = df_401_apt[df_401_apt['energieverbruik'] <= (ondergrens_verbruik * afstand_in_km)]
    indexen_voor_false += list(df_checked.index)
    #bovengrens
    df_checked = df_401_apt[df_401_apt['energieverbruik'] >= (bovengrens_verbruik * afstand_in_km)]
    indexen_voor_false += list(df_checked.index)
    
    # dienstrit ehvbst- ehvapt lijn 401
    afstand_in_km = int(df_afstanden.loc[3, 'afstand in meters']/1000)
    df_401 = df[df['buslijn'] == 401.0]
    df_401_bst = df_401[df_401['startlocatie'] == 'ehvbst']
    #ondergrens
    df_checked = df_401_bst[df_401_bst['energieverbruik'] <= (ondergrens_verbruik * afstand_in_km)]
    indexen_voor_false += list(df_checked.index)
    #bovengrens
    df_checked = df_401_bst[df_401_bst['energieverbruik'] >= (bovengrens_verbruik * afstand_in_km)]
    indexen_voor_false += list(df_checked.index)
    
    # materiaalrit ehvbst - ehvapt en terug zijn hetzelfde
    afstand_in_km = int(df_afstanden.loc[4, 'afstand in meters']/1000)
    df_materiaal = df[df['activiteit'] == 'materiaal rit']
    # heen
    df_mat_apt = df_materiaal[df_materiaal['startlocatie'] == 'ehvapt']
    df_mat_apt_bst = df_mat_apt[df_mat_apt['eindlocatie'] == 'ehvbst']
    
    df_checked = df_mat_apt_bst[df_mat_apt_bst['energieverbruik'] <= (ondergrens_verbruik * afstand_in_km)]
    indexen_voor_false += list(df_checked.index)
    df_checked = df_mat_apt_bst[df_mat_apt_bst['energieverbruik'] >= (bovengrens_verbruik * afstand_in_km)]
    indexen_voor_false += list(df_checked.index)
    # terug
    df_mat_bst = df_materiaal[df_materiaal['startlocatie'] == 'ehvbst']
    df_mat_bst_apt = df_mat_bst[df_mat_bst['eindlocatie'] == 'ehvapt']
    
    df_checked = df_mat_bst_apt[df_mat_bst_apt['energieverbruik'] <= (ondergrens_verbruik * afstand_in_km)]
    indexen_voor_false += list(df_checked.index)
    df_checked = df_mat_bst_apt[df_mat_bst_apt['energieverbruik'] >= (bovengrens_verbruik * afstand_in_km)]
    indexen_voor_false += list(df_checked.index)
    
    # materiaalrit ehvbst - ehvgar en terug zijn hetzelfde
    afstand_in_km = int(df_afstanden.loc[6, 'afstand in meters']/1000)
    #heen
    df_mat_bst_gar = df_mat_bst[df_mat_bst['eindlocatie'] == 'ehvgar']
    
    df_checked = df_mat_bst_gar[df_mat_bst_gar['energieverbruik'] <= (ondergrens_verbruik * afstand_in_km)]
    indexen_voor_false += list(df_checked.index)
    df_checked = df_mat_bst_gar[df_mat_bst_gar['energieverbruik'] >= (bovengrens_verbruik * afstand_in_km)]
    indexen_voor_false += list(df_checked.index)
    # terug
    df_mat_gar = df_materiaal[df_materiaal['startlocatie'] == 'ehvgar']
    df_mat_gar_bst = df_mat_gar[df_mat_gar['eindlocatie'] == 'ehvbst']
    
    df_checked = df_mat_gar_bst[df_mat_gar_bst['energieverbruik'] <= (ondergrens_verbruik * afstand_in_km)]
    indexen_voor_false += list(df_checked.index)
    df_checked = df_mat_gar_bst[df_mat_gar_bst['energieverbruik'] >= (bovengrens_verbruik * afstand_in_km)]
    indexen_voor_false += list(df_checked.index)
    
    # materiaalrit ehvapt - ehvgar en terug zijn hetzelfde
    afstand_in_km = int(df_afstanden.loc[8, 'afstand in meters']/1000)
    # heen
    df_mat_apt_gar = df_mat_apt[df_mat_apt['eindlocatie'] == 'ehvgar']
    
    df_checked = df_mat_apt_gar[df_mat_apt_gar['energieverbruik'] <= (ondergrens_verbruik * afstand_in_km)]
    indexen_voor_false += list(df_checked.index)
    df_checked = df_mat_apt_gar[df_mat_apt_gar['energieverbruik'] >= (bovengrens_verbruik * afstand_in_km)]
    indexen_voor_false += list(df_checked.index)
    # terug
    df_mat_gar_apt = df_mat_gar[df_mat_gar['eindlocatie'] == 'ehvapt']
    
    df_checked = df_mat_gar_apt[df_mat_gar_apt['energieverbruik'] <= (ondergrens_verbruik * afstand_in_km)]
    indexen_voor_false += list(df_checked.index)
    df_checked = df_mat_gar_apt[df_mat_gar_apt['energieverbruik'] >= (bovengrens_verbruik * afstand_in_km)]
    indexen_voor_false += list(df_checked.index)
    return indexen_voor_false

def efficientie_maar_dan_gemiddeld(bussen:list[object]):
    totaal = 0
    for bus in bussen:
        totaal += bus.efficientie
    verhouding = totaal/len(bussen)
    return verhouding