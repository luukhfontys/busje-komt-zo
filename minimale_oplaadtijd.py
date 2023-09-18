import pandas as pd
from datetime import datetime

df_planning = pd.read_excel('omloop planning.xlsx')
tijden = []

starttijd = df_planning.starttijd.values.tolist()
eindtijd = df_planning.eindtijd.values.tolist()
activiteit = df_planning.activiteit.values.tolist()

index = 0

for i in activiteit:
    if i == 'opladen':
        start_time = starttijd[index]
        end_time = eindtijd[index]
        t2 = datetime.strptime(end_time, "%H:%M:%S")
        t1 = datetime.strptime(start_time, "%H:%M:%S")
        delta = t2-t1
        sec = delta.total_seconds()
        min = sec / 60
        if min <= 15:
            print('Bus laat te kort op')
        
    index += 1