from Planning_functies import bepaal_energieverbruik
import pandas as pd
df = pd.read_excel('Connexxion data - 2023-2024.xlsx')

class lege_bus:
    def __init__(self, batterij:float, omloopnummer:int):
        self.starttijden = []
        self.eindtijden = []
        self.start_locaties = []
        self.eind_locaties = []
        self.batterijstart = batterij
        self.batterijmin = 0.1 * batterij
        self.activiteit = []
        self.buslijn = []
        self.energie_verbruik = []
        self.omloopnummer = omloopnummer
        self.batterij_huidig = batterij
        self.locatie_huidig = 'ehvgar'
        
    def toevoegen_rit(self, starttijd, eindtijd, start_locatie, eind_locatie, verbruik, activiteit, buslijn=''):
        check = self.controleer_verbruik()
        if not check[0]:
            return False
        self.update_waardes(starttijd=starttijd, eindtijd=eindtijd, start_locatie=start_locatie, eind_locatie=eind_locatie, verbruik=verbruik, activiteit=activiteit, buslijn=buslijn)
        self.locatie_huidig = eind_locatie
        return True
    
    def update_waardes(self, starttijd, eindtijd, start_locatie, eind_locatie, verbruik, activiteit, buslijn=''):
        self.starttijden.append(starttijd)
        self.eindtijden.append(eindtijd)
        self.start_locaties.append(start_locatie)
        self.eind_locaties.append(eind_locatie)
        self.energie_verbruik.append(verbruik)
        self.activiteit.append(activiteit)
        self.buslijn.append(buslijn)
    

    def controleer_verbruik(self, verbruik1, verbruik2, verbruik3):
        

        
    

        
        