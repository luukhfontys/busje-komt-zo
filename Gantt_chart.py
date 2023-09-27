import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

def Gantt_chart(omloop_planning: pd.DataFrame):
    """"Vul path naar omloop planning in, output: een plotly gantt chart object."""
    df_planning = omloop_planning
    df = omloop_planning

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


    y_label = {'omloop nummer': 'Omloop nummer'}

    colors = {"materiaal rit": "forestgreen", "opladen": "darkgray", 401: "cornflowerblue", 400.0: "steelblue"}

    fig = px.timeline(df, x_start="starttijd datum", x_end="eindtijd datum", y="omloop nummer", color = 'activiteit', title = "Gantt Chart", labels = y_label, color_discrete_map = colors)
    fig.update_layout(xaxis_title="Date")

    return fig