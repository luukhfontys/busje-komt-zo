from datetime import datetime

class bus:
    '''
    Blauwdruk voor een bus,
    hiermee kan voor een bus het volgende bij gehouden worden:
        - De tijden waarop een bus vertrekt en de tijden waarop een bus aankomt
        - De locaties waarvan een bus vertrekt en waar een bus heen rijd en onder welke dienstrit deze valt
        - De activeit waaronder een rit valt
        - Het energie verbruik van een rit
        - Het nummer van de bus (in de excel naar gerefereerd als omloopnummer)
    
    ''' 
    def __init__(self, tijden:list[tuple[str,str]]=list(), locaties:list[tuple]=list(), activiteit:list[str]=list(),
                 buslijn:list[float]=list(), energieverbruik:list[float]=list(), omloopnummer:int=0,
                 batterij:tuple[float,float]=tuple()):
        '''
        Het meegeven van waardes bij het aanmaken van een classobject van de class bus
        Hier in word mee gegeven:
            - de tijden, start en eind als tuple in een lijst. Deze staan namelijk vast en dit maakt dit een fijne opslagmethode
              op deze manier kun je ze als paar naar voren halen.
            - Voor locaties gebruiken wij dezelfde opslagstructuur omdat deze ook vast staan als paar
            - De activiteit word een lijst met strings
            - De buslijn word een lijst met floats, ondanks dat onze buslijnen gehele getallen zijn ziet python NaN als een float,
              hierdoor is onze hele lijst hetzelfde
            - Energieverbuik is een list met floats, vanzelfsprekend gezien de input data
            - het omloop nummer is een int, word gebruikt om makkelijk te weten naar welke bus we referen
            - De batterij word weer gegeven als een tuple, hierin vinden we de start waarde van de batterij en
              de minimale waarde van de batterij, wederom staan deze vast vandaar de tuple
              batterij word opgedeeld in twee delen, batterij start en batterijhuidig, dit is handiger voor later
              bij het opstellen van de class word de start waarde mee gegeven als huidige batterij
            
            
        We geven elk argument een lege versie mee als deze word vergeten,
        op deze manier kunnen we specifieker aangeven waaraan te kort word geschoten in geval van een error
        Inplaats van:
        y agruments expected x
        krijgen we:
        Er is geen lijst met buslijnen meegegeven.
        Dit gaan we doen door middel van:  assert Statement: -> error return
        '''
        # nu worden alle eigenschappen mee gegeven, self refereert naar deze class instantie,
        # daarnaast krijgt elke eigenschap dezelfde naam als het argument uit de __init__,
        # hierdoor werkt de class intuitief
        # met assert forceren we dat alle gegevens in de juiste vorm staan,
        # op deze manier kunnen we specifieke feedback geven op de fout waar het programma tegen aanloopt
        assert len(tijden) > 0, 'Er zijn geen tijden meegegeven' # controleer of tijden niet leeg is daarna voor de andere gegevens
        assert len(locaties) > 0, 'Er zijn geen tijden meegegeven'
        assert len(activiteit) > 0, 'Er zijn geen activiteiten meegegeven'
        assert len(buslijn) > 0, 'Er zijn geen buslijnen meegegeven'
        assert len(energieverbruik) > 0, 'Er is geen energieverbruik meegegeven'
        assert omloopnummer > 0, 'Er is geen omloop nummer mee gegeven'
        assert len(batterij) == 2, 'Er zijn niet genoeg batterij waarde meegegeven'
        assert len(tijden) == len(locaties) == len(activiteit) == len(buslijn) == len(energieverbruik), 'De lijsten zijn niet evenlang'
        # ^^ controleer of de lijsten even lang zijn, zo voorkomen we dat de for loop een error geeft
        self.tijden = tijden
        self.locaties = locaties 
        self.activiteit = activiteit
        self.buslijn = buslijn
        self.energieverbruik = energieverbruik
        self.omloopnummer = omloopnummer
        self.batterijstart = batterij
        self.batterijhuidig = batterij[0] # hier word batterij geindexed omdat batterij een tweedelige tuple behoort te zijn
        
        self.onderbouwing = ' ' # hierin slaan we de string op die uitleg geeft over de reden van falen,
                                # als de bus zijn rit kan rijden blijf deze leef, maar deze moet bestaan om er naar te refereren
        self.valide = self.check_bus() # hier roepen we de functie check bus aan om te controleren of deze rit valide is,
                                       # dit gebeurt na het mee geven van de eigenschappen zodat we deze kunnen gebruiken
        
        # meegegeven gegevens staan beschreven in de class docstring #
        
        
    def check_bus(self)->int:
        '''
        Het controleren of een bus voldoet aan de eisen voor de planning
        Hierbij word rekening gehouden met:
            - De verbruik van de bus
            - De tijden van de bus rit
            - De minimale laadtijd
        
        De functie retourneerd een 0 in het geval de de bus niet aan de bovenstaande eisen voldoet,
        Wanneer de bus wel aan de bovenstaande eisen voldoet retourneerd de functie een 1
        '''
        # we controleren alle drie de criteria per iteratie
        
        for rit in range(len(self.tijden)): # we gebruiken hier self.tijden maar de lijsten zijn allemaal evenlang
            self.batterijhuidig -= self.energieverbruik[rit] # updaten van de batterij, 
                                                             #na de __init__ is huidige batterij de eindstand van de batterij
            ## batterij check
            if self.batterijhuidig <= self.batterijstart[1]: # index 1 is de min waarde van de batterij uit batterijstart
                self.onderbouwing = (
                    f'''Battery of bus {self.omloopnummer} went below the minimum threshold between {self.tijden[rit][0]} and {self.tijden[rit][1]}
                    '''
                    ) # onderbouwing voor invalide planning
                return 0 # returnen nul zodat er gesorteerd kan worden
            ## Tijd check
            if rit-1 >= 0: # dan is het niet de eerste rit dus moet er gecheckt worden of het haalbaar is
                vorige_eindtijd = self.tijden[rit-1][1] # we halen de tuple uit de lijst en daarna de eind tijd uit de tuple
                                                        # we kijken naar de eindtijd van de vorige rit dus rit -1 als index
                huidige_starttijd = self.tijden[rit][0] # we halen de tuple uit de lijst en daarna de start tijd uit de tuple
                if vorige_eindtijd != huidige_starttijd: # als deze niet hetzelfde zijn moeten we kijken of er overlap is
                    gesplite_eindtijd = vorige_eindtijd.split(':') # ze zijn opgeslagen als str dus gebruiken we split
                    gesplite_begintijd = huidige_starttijd.split(':') # datetime werkt hier niet omdat datetime
                                                                      # alleen negatieve waarde kan hebben voor dagen
                    
                    if (
                        (int(gesplite_eindtijd[0])%24 > int(gesplite_begintijd[0])%24) or
                        (int(gesplite_eindtijd[0]) == int(gesplite_begintijd[0]) and
                        int(gesplite_eindtijd[1]) > int(gesplite_begintijd[1]))
                        ): # we checken 2 scenario's:
                           # - is het uur van de vorige tijd later dan de huidige modulo 24 om met de nacht rekening te houden
                           # - zijn ze hetzelfde checken we om de zelfde manier de minuten
                        self.onderbouwing = f'bus {self.omloopnummer} returns to late from ride {rit-1} to make ride {rit} in time'
                        return 0
            ## minimale laad tijd check
            if self.activiteit[rit] == 'opladen': # checken of we moeten controleren
                begintijd = self.tijden[rit][0]
                eindtijd = self.tijden[rit][1]
                begintijd_datetime = datetime.strptime(begintijd, "%H:%M:%S") # tijd omzetten naar datetime constructie
                eindtijd_datetime = datetime.strptime(eindtijd, "%H:%M:%S")
                delta = eindtijd_datetime - begintijd_datetime # timedelta object crëeeren
                minutes = (delta.total_seconds())/60 # aantal minuten bepalen
                if minutes <= 15: # controle voor minimum tijd
                    self.onderbouwing = f'bus {self.omloopnummer} charges for to little time during ride {rit + 1}'
                    return 0
            else:
                continue
        return 1
        
    def __lt__(self,other):
        '''
        De class functie __lt__ laat ons class objecten van dezelfde class vergelijken om een gedefinëerde waarde
        Self verwijst naar dit class object en other naar een class object van dezelfde class.
        Doordat we nu class objecten kunnen vergelijken kunnen wij een lijst met class objecten sorteren.
        In deze functie sorteren wij de class objecten op de uitkomst van checkbus
        '''
        return self.valide < other.valide # aangeven welke waarde binnen de class vergeleken dient te worden
    