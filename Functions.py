import pandas as pd
import numpy as np

def format_check_omloop(df_planning):
    header_format = ['startlocatie', 'eindlocatie', 'starttijd', 
                     'eindtijd','activiteit', 'buslijn', 
                     'energieverbruik', 'starttijd datum',
                     'eindtijd datum', 'omloop nummer']
    df_headers = df_planning.columns.values[1:].tolist()
    type_format = [str, str, str, str, str, (np.int64, np.float64), (np.int64, np.float64), pd.Timestamp, pd.Timestamp, (int, float, np.int64)]
    df_types = df_planning.iloc[1][1:]

    if header_format == df_headers: header_check = True

    type_check = True
    for i in range(len(type_format)):
        if not isinstance(df_types[i], type_format[i]):
            type_check = False
            
    return all([header_check, type_check])

def prestatiemaat_materiaal_minuten(df_planning: pd.DataFrame) -> tuple[float, float]:
    """
    Deze functie neemt de omloop planning in vorm van pandas dataframe en output vervolgens
    de totale minuten dat er materiaal ritten zijn gereden en het gemiddelde aantal minuten dat een omloop
    materiaal ritten rijdt.
    """
    #Filteren op alleen de materiaal ritten
    df_materiaal_ritten = df_planning[df_planning['activiteit'] == 'materiaal rit']

    #Convert de datum columns naar een datetime object m.b.v. pandas
    df_materiaal_ritten['starttijd datum'] = pd.to_datetime(df_materiaal_ritten['starttijd datum'])
    df_materiaal_ritten['eindtijd datum'] = pd.to_datetime(df_materiaal_ritten['eindtijd datum'])
    
    #Maakt vervolgens 2 nieuwe columns die de datums naar epoch tijd omzetten.
    df_materiaal_ritten['epoch_starttijd'] = df_materiaal_ritten['starttijd datum'].apply(lambda x: x.timestamp())
    df_materiaal_ritten['epoch_eindtijd'] = df_materiaal_ritten['eindtijd datum'].apply(lambda x: x.timestamp())

    #Neemt het verschil in tijd tussen start en eind en deelt door 60 om de minuten te krijgen voor elke materiaal rit.
    df_materiaal_ritten['Materiaal Rit lengte minuten'] = (df_materiaal_ritten['epoch_eindtijd'] - df_materiaal_ritten['epoch_starttijd']) / 60
    
    #Hier berekenen we het totale en gemiddelde van de materiaal ritten en stoppen ze in passende variabelen
    totale_minuten = df_materiaal_ritten['Materiaal Rit lengte minuten'].sum()
    
    #df_materiaal_grouped slaat voor elke bus apart de materiaal rit lengte op.
    df_materiaal_grouped = df_materiaal_ritten.groupby('omloop nummer')['Materiaal Rit lengte minuten'].sum()
    
    #Algemene gemiddelde materiaal rit lengte voor alle bussen: 
    gem_minuten_bus = df_materiaal_grouped.mean()

    return totale_minuten, gem_minuten_bus

def aantal_omlopen(df_planning: pd.DataFrame) -> int:
    """Telt het aantal omlopen in een gegeven omloopplanning."""
    
    #Pakt het aantal unieke omloopnummers en telt ze op.
    omloop_aantal = len(df_planning['omloop nummer'].unique())
    
    return omloop_aantal

def prestatiemaat_speling(df_planning: pd.DataFrame) -> tuple[float, float, float]:
    
    #Convert de datum columns naar een datetime object m.b.v. pandas
    df_planning['starttijd datum'] = pd.to_datetime(df_planning['starttijd datum'])
    df_planning['eindtijd datum'] = pd.to_datetime(df_planning['eindtijd datum'])
    
    #Maakt vervolgens 2 nieuwe columns die de datums naar epoch tijd omzetten.
    df_planning['epoch_starttijd'] = df_planning['starttijd datum'].apply(lambda x: x.timestamp())
    df_planning['epoch_eindtijd'] = df_planning['eindtijd datum'].apply(lambda x: x.timestamp())

    #Alle minuten tellen die niet zijn aangegeven door de telkens de eindtijd en de start tijd te vergelijken van de op een volgende ritten.
    df_planning['Verschil met volgende'] = (df_planning['epoch_starttijd'].iloc[1:].reset_index(drop=True) - df_planning['epoch_eindtijd'].iloc[:-1].reset_index(drop=True)) / 60
   
    #Uitzoeken waar de bussen van id veranderen in de dataframe en die verschil waardes naar 0 zetten
    mask = df_planning['omloop nummer'] != df_planning['omloop nummer'].shift(-1)
    switch_indices = df_planning.index[mask][:-1]
    df_planning.loc[switch_indices, 'Verschil met volgende'] = 0

    #Tel alle niet aangeven minuten bij elkaar op
    totaal_niet_aangegeven_minuten = df_planning['Verschil met volgende'].sum()
    
    #Bereken idle tijd net als bij materiaal ritten
    df_idle = df_planning[df_planning['activiteit'] == 'idle']
    df_idle['idle lengte minuten'] = (df_idle['epoch_eindtijd'] - df_idle['epoch_starttijd']) / 60
    totale_idle_minuten = df_idle['idle lengte minuten'].sum()
    
    #Bereken idle tijd per bus.
    df_idle_grouped = df_idle.groupby('omloop nummer')['idle lengte minuten'].sum()
    
    #Bereken algemene gemiddelde idle tijd per bus
    gem_minuten_idle_bus = df_idle_grouped.mean()
    
    return totaal_niet_aangegeven_minuten, totale_idle_minuten, gem_minuten_idle_bus