import pandas as pd
from bus_class import bus

def to_class(df:pd.DataFrame, batterij_waarde:tuple[float,float]=(270,27.0)):
    batterij = batterij_waarde
    bussen = []
    for omloop in range(1,max(df.loc[:,'omloop nummer'])):
        locaties, tijden, activiteiten, buslijnen, energieverbruik = to_class_format(df,omloop)
        bussen.append(bus(tijden=tijden,
                          locaties=locaties,
                          activiteit=activiteiten,
                          buslijn=buslijnen,
                          energieverbruik=energieverbruik, 
                          omloopnummer=omloop,
                          batterij=batterij
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