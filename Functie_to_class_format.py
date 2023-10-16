import pandas as pd
from bus_class import bus

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
    df_planning.drop(['Unnamed: 0', 'eindtijd', 'energieverbruik', 'starttijd datum', 'eindtijd datum', 'omloop nummer', 'activiteit'],axis='columns', inplace=True)
    df_dienstregeling.rename(columns={'vertrektijd':'starttijd'}, inplace=True)
    while compleet and iteration < maximum:
        #print(df_dienstregeling.loc[iteration, :])
        nieuwe_rij = df_dienstregeling.loc[iteration, :]
        nieuwe_rij.iloc[1] += ':00' 
        df_planning.loc[len(df_planning.index)] = nieuwe_rij
        dupes = list(df_planning.duplicated(keep='first'))
        print(type(dupes))
        if dupes[-1] == 0:
            print(nieuwe_rij)
            compleet = False
        else:
            df_planning.drop_duplicates(inplace=True)
            print(df_planning)
            #compleet = False
            iteration += 1
    return compleet