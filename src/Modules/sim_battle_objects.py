from Modules.sim_objects import Faction, Region, UnitType, Board,CampaignType
from colorama import Style



class Campaign():
    def __init__ (self,board:Board,region:Region,campaign_type:CampaignType):
        self.faction_units = {}
        self.region = region
        self.board = board
        self.factions = []
        self.campaign_type = campaign_type
    
    def join_campaign(self,faction:Faction):
        if faction in self.factions:
            raise Exception(f"{faction} has already joined the campaign on {self.region}. A faction can only join a campaign once")
        self.factions.append(faction)
        
    
    def add_faction_units(self,faction: Faction, units: dict):
        if faction not in self.factions:
            raise Exception(f"{faction} is not in the campaign")
        for unit in units:
            if unit not in UnitType:
                raise Exception(f"{unit} is not a valid unit type")
            unit_count = units[unit]
            
            for faction_unit in faction.units:
                try:
                    if faction_unit.name.name == unit.name:
                        faction_unit.remove_units(unit_count)
                except Exception as e:
                    raise Exception("Cannot add more faction units than you have.")

            print (f"{faction} has added {unit_count} {unit.name} to the campaign on {self.region}")
        if faction.name not in self.faction_units:
            self.faction_units[faction.name] = units
        else: 
            self.faction_units[faction.name][UnitType.ARCHER] += units[UnitType.ARCHER]
            self.faction_units[faction.name][UnitType.SWORDSMAN] += units[UnitType.SWORDSMAN]
            self.faction_units[faction.name][UnitType.CAVALRY] += units[UnitType.CAVALRY]


    def get_faction_units(self):
        print("-----------------------------------")
        for faction in self.faction_units:
            for enlisted_faction_unit in self.faction_units[faction]:
                print(f"{faction} has {self.faction_units[faction][enlisted_faction_unit]} {enlisted_faction_unit.name} units in the campaign on {self.region}")
            print("+++++++++++++++++++++++++++++++++++")
        print("-----------------------------------")

