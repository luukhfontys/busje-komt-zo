# een functie bestand om te importeren voor de planning
import pandas as pd

def inladen_data(bestandsnaam:str, sheetnaam_sheet_1:str, sheet_naam_sheet_2:str)->[pd.DataFrame, pd.DataFrame]:
    Dienstregeling = pd.read_excel(bestandsnaam, sheet_name=sheetnaam_sheet_1)
    afstands_matrix = pd.read_excel(bestandsnaam, sheet_name=sheet_naam_sheet_2)
    return Dienstregeling, afstands_matrix

def bepaal_energieverbruik(afstands_matrix:pd.DataFrame, startlocatie:str, eindlocatie:str,verbruik:float ,buslijn:float='nvt')->float:
    start_locaties = afstands_matrix[afstands_matrix['startlocatie'] == startlocatie]
    combinaties = start_locaties[start_locaties['eindlocatie'] == eindlocatie]
    if buslijn == 'nvt':
        return verbruik * combinaties['afstand in meters'].tolist()[-1]
    else:
        juiste_lijn = combinaties[combinaties['buslijn']==buslijn]
        return verbruik * juiste_lijn['afstand in meters'].tolist()[-1]
    

def bepaal_eindtijd(afstands_matrix:pd.DataFrame, startlocatie:str, eindlocatie:str, starttijd ,buslijn:float='nvt')->float:
    start_locaties = afstands_matrix[afstands_matrix['startlocatie'] == startlocatie]
    combinaties = start_locaties[start_locaties['eindlocatie'] == eindlocatie]
    if buslijn == 'nvt':
        min_reistijd = combinaties['min reistijd in min'].tolist()[-1]
        max_reistijd = combinaties['max reistijd in min'].tolist()[-1]
        reistijd = (min_reistijd + max_reistijd)/2
    else:
        juiste_lijn = combinaties[combinaties['buslijn']==buslijn]
        min_reistijd = juiste_lijn['min reistijd in min'].tolist()
        max_reistijd = juiste_lijn['max reistijd in min'].tolist()
        reistijd = (min_reistijd + max_reistijd)/2

    return starttijd + reistijd