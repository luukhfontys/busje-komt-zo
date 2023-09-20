import pandas as pd
from datetime import datetime

df_planning = pd.read_excel('omloop planning.xlsx')


def minimale_oplaadtijd(minimale_lengte_oplaadtijd):
    """
        Geeft aan of een bus wel voldoet aan de minimale oplaadtijd.
         
        input: Minimale oplaadtijd in minuten 
        Output: Voldoet de bus aan de minimale oplaadtijd """
    
    starttijd = df_planning.starttijd.values.tolist()
    eindtijd = df_planning.eindtijd.values.tolist()
    activiteit = df_planning.activiteit.values.tolist()

    index = 0

    for i in activiteit:
        #Met deze forloop wordt gekeken wat de oplaadtijd per oplaadbeurt is 
        if i == 'opladen':
            start_time = starttijd[index]
            end_time = eindtijd[index]
            t2 = datetime.strptime(end_time, "%H:%M:%S")
            t1 = datetime.strptime(start_time, "%H:%M:%S")
            #Berekent de verschil in tijd
            delta = t2-t1
            #Rekent de oplaadtijd om in seconden
            sec = delta.total_seconds()
            minuten = sec/60

            if minuten < minimale_lengte_oplaadtijd:
                print('Bus laad te kort op')
        
        index += 1


minimale_oplaadtijd(15)