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
        
    def toevoegen_rit(self):
        check = self.controleer_verbruik()
        if not check:
            return False
        else:
            'snaaien gvd, verdomme milou'
        return
    
    def controleer_verbruik(self):
        print('Help Paul gaat slaan')
        
        