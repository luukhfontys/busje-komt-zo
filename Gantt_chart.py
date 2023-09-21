import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

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





import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

df["starttijd datum"] = pd.to_datetime(df["starttijd datum"])
df["eindtijd datum"] = pd.to_datetime(df["eindtijd datum"])

def create_gantt_chart(df, buslijn):
    fig, ax = plt.subplots(figsize=(12, 6))

    for index, row in df.iterrows():
        ax.barh(
            y=row["activiteit"],
            left=row["starttijd datum"],
            width=row["eindtijd datum"] - row["starttijd datum"],
            align="center"
        )

    ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    ax.set_xlabel("Tijd")
    ax.set_ylabel("Activiteit")
    ax.set_title(f"Gantt-diagram voor Buslijn {buslijn}")
    plt.legend()

    plt.tight_layout()
    plt.show()

for buslijn in df["buslijn"].unique():
    df_buslijn = df[df["buslijn"] == buslijn]
    create_gantt_chart(df_buslijn, buslijn)