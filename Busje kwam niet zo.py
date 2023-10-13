class bus:
    def __init__(self, tijden:list=[], locaties:list=[], activiteit:list=[], 
                 buslijn:list=[], energieverbruik:list=[], omloopnummer:int=0, 
                 batterijstart:float=0.0, batterijmin:int=30) -> None:
        self.tijden = tijden
        self.locaties = locaties
        self.activiteit = activiteit
        self.buslijn = buslijn
        self.energieverbruik = energieverbruik
        self.omloopnummer = omloopnummer
        self.batterijstart = batterijstart
        self.batterijmin = batterijmin

    def check_bus(self):
        batterij = self.batterijstart
        succes = 0
        for rit in range(len(self.tijden)):
            batterij -= self.energieverbruik[rit]
            if batterij <= self.batterijmin:
                print(f'batterij is onder het minimum gegaan bij rit type {self.activiteit[rit]} tussen de tijden {self.tijden[rit][0]} en {self.tijden[rit][1]} voor omloop {self.omloopnummer}')
                succes = 1
                break
        if succes == 0:    
            print(f'omloop {self.omloopnummer} had genoeg batterij om de omloop te rijden')

bussen = []
import pandas as pd
df_planning = pd.read_excel('omloop planning.xlsx')
omloopnummers = set(df_planning.loc[:,'omloop nummer'])
for omloop in omloopnummers:
    df_temp = df_planning[df_planning['omloop nummer'] == omloop]
    tijden = []
    locaties = []
    activiteit = []
    energieverbruik = []
    buslijn = []
    batterijstart = 285
    for i in df_temp.index:
        tijden.append((df_temp.loc[i,'starttijd'][:-3],df_temp.loc[i,'eindtijd'][:-3]))
        locaties.append((df_temp.loc[i,'startlocatie'],df_temp.loc[i,'eindlocatie']))
        activiteit.append(df_temp.loc[i,'activiteit'])
        energieverbruik.append((df_temp.loc[i,'energieverbruik']))
        buslijn.append(df_temp.loc[i,'buslijn'])
        
    x = bus(tijden=tijden,locaties=locaties,activiteit=activiteit,energieverbruik=energieverbruik,buslijn=buslijn,omloopnummer=omloop,batterijstart=batterijstart)
    bussen.append(x)
for omloop in bussen:
    omloop.check_bus()
