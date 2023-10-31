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
        
    def toevoegen_rit(self, starttijd, eindtijd, start_locatie, eind_locatie, verbruik1,  verbruik2, verbruik3, buslijn=''):
        check = self.controleer_verbruik(verbruik1=verbruik1, verbruik2=verbruik2, verbruik3=verbruik3)
        if not check:
            return False
        if self.locatie_huidig != start_locatie:
            self.update_waardes(starttijd=starttijd, eindtijd=eindtijd,
                            start_locatie=self.locatie_huidig, eind_locatie=start_locatie,
                            verbruik=verbruik3, activiteit='Materiaal rit') #### start tijd aanpassen!!!!
            
        self.update_waardes(starttijd=starttijd, eindtijd=eindtijd,
                            start_locatie=start_locatie, eind_locatie=eind_locatie,
                            verbruik=verbruik1, activiteit='Dienst rit', buslijn=buslijn)
        
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
    

    def controleer_verbruik(self, verbruik1, verbruik2, verbruik3=0.0):
        totaal_verbruik = verbruik1 + verbruik2 + verbruik3
        if (self.batterij_huidig - totaal_verbruik) >= self.batterijmin:
            return True
        else:
            return False

        

        
    

        
        