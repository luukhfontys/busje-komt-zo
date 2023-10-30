from Planning_class import lege_bus
import Planning_functies
import pandas as pd
df = pd.read_excel('Connexxion data - 2023-2024.xlsx')


x = lege_bus(batterij=100.0, omloopnummer=1)
x.controleer_verbruik()