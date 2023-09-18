import pandas as pd

planning = pd.read_excel('omloop planning.xlsx')

class bus:
    def __init__(self, rit, locatie, batterij):
        self.rit = rit
        self.locatie = locatie
        self.batterij = batterij
    def __repr__(self) -> str:
        return print(f'Rit: {self.rit}\nLocatie: {self.locatie}\nBatterij: {self.batterij} ')
