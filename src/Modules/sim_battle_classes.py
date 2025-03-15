from Modules.sim_objects import Faction, Region, UnitType, Board

class Campaign():
    def __init__ (self,board:Board,region:Region):
        self.battles = []
        self.faction_units = {}
        self.region = region
        self.board = board
        self.factions = [self.board.faction_turn]
    
    def join_campaign(self,faction:Faction):
        if faction in self.factions:
            raise Exception(f"{faction} has already joined the campaign")
        self.factions.append(faction)
        print(f"{faction} has joined the campaign on {self.region}")
        
    
    def add_faction_units(self,faction: Faction, units: dict):
        if faction not in self.factions:
            raise Exception(f"{faction} is not in the campaign")
        for unit in units:
            if unit not in UnitType:
                raise Exception(f"{unit} is not a valid unit type")
            unit_count = units[unit]
            if (unit_count > faction.units[unit].count):
                raise Exception(f"{faction} does not have enough {unit.name} units to add to the campaign")
            faction.units[unit].remove_units(unit_count)
            print (f"{faction} has added {unit_count} {unit.name} to the campaign on {self.region}")


        self.faction_units[faction.name] = units

    def get_faction_units(self):
        for faction in self.faction_units:
            for enlisted_faction_unit in self.faction_units[faction]:
                print(f"{faction} has {self.faction_units[faction][enlisted_faction_unit]} {enlisted_faction_unit.name} units in the campaign on {self.region}")
