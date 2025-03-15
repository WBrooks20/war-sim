from enum import Enum
import random
from colorama import Fore, Back, Style

# Define the phases of the game
class Phase(Enum):
    ACTION = 1
    BATTLE = 2

#define the unit types
class UnitType(Enum):
    ARCHER = 0
    SWORDSMAN = 1
    CAVALRY = 2

class Actions(Enum):
    RECRUIT = 0
    ATTACK = 1
    DEFEND = 2

# Define the board class to manage the game state
class Board:
    def __init__(self):
        self.faction_turn = None
        self.faction_action_count = 3
        self.current_phase = Phase.ACTION
        self.regions = []
        self.factions = []
        self.turn_eligible_factions = []
        self.year = None
        self.board_fore_style_color = Fore.WHITE
    
    def __repr__(self) -> str:
        return (f"{self.board_fore_style_color}Starting faction: {self.faction_turn}\n{self.board_fore_style_color}Year: {self.year}\n"
                f"{self.board_fore_style_color}Regions: {self.regions}\nFactions: {self.factions}\n"
                f"{self.board_fore_style_color}Phase: {self.current_phase.name}\nTurn eligible factions: {self.turn_eligible_factions}\n{self.board_fore_style_color}"
                "-----------------------------------")

    def init_board(self, regions: list, factions: list, year: int) -> None:
        self.regions = regions
        self.factions = factions
        self.year = year
        self.faction_action_count = 3
        self.turn_eligible_factions = list(self.factions)
        start_faction = random.choice(self.turn_eligible_factions)
        self.turn_eligible_factions.remove(start_faction)
        self.faction_turn = start_faction
        print(self)
    
    def update_state(self) -> None:
        if len(self.turn_eligible_factions) <= 0 and self.faction_action_count == 0:
            self.update_phase()
            return

        if self.faction_action_count == 0:
            self.set_faction_turn()
    
    def set_faction_turn(self) -> None:
        if not self.turn_eligible_factions:
            raise Exception("No factions are eligible for a turn.")
        faction = self.turn_eligible_factions.pop()
        if self.faction_turn == faction:
            raise Exception(f"{faction} already had a turn this year and cannot have another.")
        self.faction_turn = faction
        self.faction_action_count = 3
        print(f"Faction set to {self.faction_turn.name} with {self.faction_action_count} actions left.")
    
    def update_action_count(self,action) -> None:
        if self.current_phase != Phase.ACTION:
            raise Exception(f"The current phase is {self.current_phase}. Turns cannot happen outside of the action phase.")
        self.faction_action_count -= 1
        if self.faction_action_count < 0:
            raise Exception(f"{self.faction_turn} has no actions left.")
        print(f"{self.faction_turn} takes {action.name} action and currently has {self.faction_action_count} actions left.")
        self.update_state()
    
    def update_phase(self) -> None:
        if self.current_phase == Phase.ACTION:
            self.current_phase = Phase.BATTLE
        else:
            self.current_phase = Phase.ACTION
            self.init_board(self.regions, self.factions, self.year + 1)
        print(f"We are now in the {self.current_phase.name} phase")
    
    def get_current_faction_turn(self):
        return self.faction_turn
    
    def get_current_phase(self):
        return self.current_phase
    
    def get_current_year(self):
        return self.year
    
    def get_current_turn_eligible_factions(self):
        return self.turn_eligible_factions
    

class Faction:
    def __init__(self, name: str, regions: list):
        self.name = name
        self.regions = regions
        self.units = [Archer(), Swordsman(), Cavalry()]
        self.fore_style_colors = [Fore.RED, Fore.GREEN, Fore.BLUE, Fore.YELLOW, Fore.MAGENTA, Fore.CYAN]
        self.fore_style_color = random.choice(self.fore_style_colors)

    def __repr__(self) -> str:
        return f"{self.fore_style_color}{self.name}{Style.RESET_ALL}"
    
    def get_faction_name(self) -> str:
        return self.name
    
    def get_faction_regions(self) -> list:
        return self.regions
    
    def get_faction_units(self) -> list:
        return self.units
    

class Region:
    def __init__(self, name: str, description: str, owner: Faction):
        self.name = name
        self.description = description
        self.owner = owner
    
    def __repr__(self) -> str:
        return self.name
    
    def get_region_name(self) -> str:
        return self.name
    
    def get_region_description(self) -> str:
        return self.description
    
    def get_region_owner(self):
        return self.owner
    

class Unit:
    def __init__(self, name: UnitType, damage: int, health: int, defense: int, count: int):
        self.name = name
        self.damage = damage
        self.health = health
        self.defense = defense
        self.count = count

    def __repr__(self) -> str:
        return (f"{self.name.name}\nCount: {self.count}\nDamage: {self.damage}\n"
                f"Health: {self.health}\nDefense: {self.defense}\n"
                "-----------------------------------")
    
    def recruit_units(self, count: int) -> None:
        self.count += count
    
    def remove_units(self, count: int) -> None:
        self.count -= count
    

class Archer(Unit):
    def __init__(self):
        super().__init__(UnitType.ARCHER, 5, 3, 1, 0)


class Swordsman(Unit):
    def __init__(self):
        super().__init__(UnitType.SWORDSMAN, 2, 7, 15, 0)


class Cavalry(Unit):
    def __init__(self):
        super().__init__(UnitType.CAVALRY, 3, 7, 8, 0)