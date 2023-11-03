import pandas as pd
class scheduled_bus():
    def __init__(self, matrix:pd.DataFrame, startbattery:float):
        '''Inladen van de data
        Afstands matrix, vanaf hier naar gerefereerd als matrix:
        afstanden en tijden van een rit worden in geladen
        schedule start: dictionary met alle ritten vanaf de garage
        material info: alle materiaal ritten tussen de busstations
        charge info: alle materiaal ritten naar de garage
        schedule info 400: alle dienstrit informatie voor lijn 400
        schedule info 401: alle dienstrit informatie voor lijn 401
        schedule: een dict met als keys de starttijden van de ritten die een bus gaat rijden
        battery: de huidige waarde van de batterij, start met startwaarde
        batterymin : de minimale waarde van de batterij
        '''
        self.schedule_start = {}    
        self.material_info = {}
        self.charge_info = {}
        self.schedule_info_400 = {}
        self.schedule_info_401 = {}
        self.schedule = {}
        self.battery = startbattery
        self.batterymin = 0.1 * self.battery
        self.current_location = 'ehvgar'
        self.current_time = 0
        for line in matrix.index:
            First_location = matrix.loc[line, 'startlocatie']
            Final_location = matrix.loc[line, 'eindlocatie']
            Battery = matrix.loc[line, 'verbruik']
            Time = matrix.loc[line, 'max reistijd in min']
            Busline = matrix.loc[line, 'buslijn']
            if Busline == 400.0:
                self.schedule_info_400[First_location] = (Final_location, Battery, Time)
            elif Busline == 401.0:
                self.schedule_info_401[First_location] = (Final_location, Battery, Time)    
            elif Final_location == 'ehvgar':
                self.charge_info[First_location] = (Final_location, Battery, Time)
            elif First_location == 'ehvgar':
                self.schedule_start[Final_location] = (First_location, Battery, Time) 
            else:
                self.material_info[First_location] = (Final_location, Battery, Time)
    def add_drive(self, Time, First_location, Final_location, Busline):
        '''
        '''
        
        
        if not self.check_time(First_location=First_location, Busline=Busline, start_time=Time):
            return False
        
        elif not self.check_battery(First_location=First_location, Busline= Busline):
            print(self.battery)
            self.schedule[str(self.current_time)] = (self.current_location, 'ehvgar', 0.0)
            self.current_time += self.charge_info[First_location][2] + 30
            self.current_location = 'ehvgar'
            self.battery += 225
            return False
        else:
            self.schedule[str(Time)] = (First_location, Final_location, Busline)
            self.current_location = Final_location
            return True
    def check_battery(self, First_location, Busline):
        if Busline == 400.0:
            schedule_battery_cost = self.schedule_info_400[First_location][1]
        else:
            schedule_battery_cost = self.schedule_info_401[First_location][1]
        charge_battery_cost = self.charge_info[First_location][1]
        
        if First_location == self.current_location:
            material_battery_cost = 0
        else:
            material_battery_cost = self.material_info[First_location][1]
        
        if self.battery - (charge_battery_cost + material_battery_cost + schedule_battery_cost) < self.batterymin:
            return False
        else:
            self.battery -= (material_battery_cost + schedule_battery_cost)
            return True
    def check_time(self, First_location, Busline, start_time):
        if Busline == 400.0:
            schedule_time_cost = self.schedule_info_400[First_location][2]
        else:
            schedule_time_cost = self.schedule_info_401[First_location][2]
        
        if First_location == self.current_location:
            material_time_cost = 0
        else:
            material_time_cost = self.material_info[First_location][2]
        
        if self.current_time + material_time_cost > start_time:
            return False
        else:
            self.current_time += (material_time_cost + schedule_time_cost)
            return True
            
        
    