##### Opzet voor maken planning

# main functie met daarin:
#   import data dienstregeling (inclusief afstanden)
#   
#   maak planning met bussen (volgens pseudo code)
#
#   export naar een excel zoals de input file voor de tool
#
#

import Planning_functies as pf
import Planning_class as pc

dr, am = pf.inladen_data(bestandsnaam='Connexxion data - 2023-2024.xlsx', sheetnaam_sheet_1='Dienstregeling', sheet_naam_sheet_2='Afstand matrix')

print(pf.bepaal_energieverbruik(afstands_matrix=am, startlocatie='ehvapt',eindlocatie='ehvbst', verbruik=100.0, buslijn = 400.0))
