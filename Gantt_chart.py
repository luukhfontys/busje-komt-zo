import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

df_planning = pd.read_excel('omloop planning.xlsx')
df = pd.read_excel('omloop planning.xlsx')

starttijd = df_planning.starttijd.values.tolist()
eindtijd = df_planning.eindtijd.values.tolist()
activiteit = df_planning.activiteit.values.tolist()

index = 0
begintijd = []
lengte = []

for i in activiteit:
    start_time = starttijd[index]
    end_time = eindtijd[index]
    t2 = datetime.strptime(end_time, "%H:%M:%S")
    t1 = datetime.strptime(start_time, "%H:%M:%S")
    begintijd.append(t1)
    delta = t2-t1
    sec = delta.total_seconds()
    minuten = sec/60
    lengte.append(minuten)

    index += 1
df['begintijd'] = begintijd
df['lengte'] = lengte


df["starttijd datum"] = pd.to_datetime(df["starttijd datum"])
df["eindtijd datum"] = pd.to_datetime(df["eindtijd datum"])

df.drop(df[df['activiteit'] == 'idle'].index, inplace = True)

for index, row in df.iterrows():
    if row['activiteit'] == 'dienst rit':
        if row['buslijn'] == '400' or '401':
            value = row['buslijn']
            df.loc[index, ['activiteit']] = [value]

for index, row in df_planning.iterrows():
    bus = df_planning['omloop nummer'].loc[df_planning.index[index]]
    starttijd_nieuw = df_planning['starttijd'].loc[df_planning.index[index]]
    if index >= 1:
        vorige_index = index - 1
        vorige_eindtijd = df_planning['eindtijd'].loc[df_planning.index[vorige_index]]
        vorige_bus = df_planning['omloop nummer'].loc[df_planning.index[vorige_index]]
        if bus == vorige_bus and vorige_eindtijd > starttijd_nieuw:
            print(index, vorige_eindtijd, starttijd_nieuw)

    

y_label = {'omloop nummer': 'Omloop nummer'}

colors = {"materiaal rit": "forestgreen", "opladen": "darkgray", 401: "mediumblue", 400.0: "steelblue"}

fig = px.timeline(df, x_start="starttijd datum", x_end="eindtijd datum", y="omloop nummer", color = 'activiteit', title = "Gantt Chart", labels = y_label, color_discrete_map = colors)
fig.update_layout(xaxis_title="Date")
print(df)
#fig.show()