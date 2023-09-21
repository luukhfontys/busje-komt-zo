import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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

df['buslijn'] = df['buslijn'].fillna(999)

fig = px.timeline(df, x_start="starttijd datum", x_end="eindtijd datum", y="omloopnummer")