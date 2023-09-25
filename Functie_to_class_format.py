import pandas as pd

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