from enum import Enum
import random
from colorama import Fore,Style
from openai import OpenAI
import os
import pathlib

#Define campaign types. 
class CampaignType(Enum):
    Attack = 1
    Defend = 2

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
        self.campaigns = []
        self.winning_faction = None
        self.client = None
    
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
        print(f"{self.faction_turn.fore_style_color}{self.faction_turn} takes {action.name} action and currently has {self.faction_action_count} actions left.{Style.RESET_ALL}")
        self.update_state()
    
    def update_phase(self) -> None:
        if self.current_phase == Phase.ACTION:
            self.current_phase = Phase.BATTLE
        else:
            self.current_phase = Phase.ACTION
            self.cleanup_campaigns()
            self.init_board(self.regions, self.factions, self.year + 1)
        print(f"+++++++++++++++++++++++++++++++++++\nWe are now in the {self.current_phase.name} phase\n+++++++++++++++++++++++++++++++++++")
    
    def get_current_faction_turn(self):
        return self.faction_turn
    
    def get_current_phase(self):
        return self.current_phase
    
    def get_current_year(self):
        return self.year
    
    def get_current_turn_eligible_factions(self):
        return self.turn_eligible_factions
    
    def get_current_campaigns(self,faction):
        print("-----------------------------------")
        for campaign in self.campaigns:
            faction_names = []
            print(f"Region: {campaign.region}\ncampaign type: {campaign.campaign_type.name}\nfactions involved:")
            for factions_l in campaign.factions:
                faction_names.append(factions_l.name)
                print(f"{factions_l}")
            if faction in campaign.factions:
                print("----------------------------------")
                print(f"{faction} archers in this campaign: {campaign.faction_units[faction.name][UnitType.ARCHER]}\n{faction} swordsmen in this campaign: {campaign.faction_units[faction.name][UnitType.SWORDSMAN]}\n{faction} cavalry in this campaign: {campaign.faction_units[faction.name][UnitType.CAVALRY]}")
                faction.tell_faction_assistant(f"region:{campaign.region}\ntype:{campaign.campaign_type.name}\nfactions involved:{", ".join(faction_names)}\n{faction} archers in this campaign: {campaign.faction_units[faction.name][UnitType.ARCHER]}\n{faction} swordsmen in this campaign: {campaign.faction_units[faction.name][UnitType.SWORDSMAN]}\n{faction} cavalry in this campaign: {campaign.faction_units[faction.name][UnitType.CAVALRY]}")
                continue
            print("+++++++++++++++++++++++++++++++++++")

            faction.tell_faction_assistant(f"region:{campaign.region}\ntype:{campaign.campaign_type.name}\nfactions involved:{", ".join(faction_names)}")



    
    def remove_losing_factions(self):
        for faction in self.factions:
            if (len(faction.regions) <= 0):
                print(f"{faction} has no remaining regions and has been removed from the simulation.")
                self.factions.remove(faction)
                if faction in self.turn_eligible_factions:
                    self.turn_eligible_factions.remove(faction)
                self.init_board(self.regions,self.factions,self.year)
    
    def cleanup_campaigns(self):
        for campaign in self.campaigns:
            if campaign.campaign_type == CampaignType.Attack:
                self.campaigns.remove(campaign)
            for faction in campaign.factions: 
                if faction not in self.factions:
                    self.campaigns.remove(campaign)
                    continue
                if campaign.faction_units[faction.name][UnitType.ARCHER] == 0 and campaign.faction_units[faction.name][UnitType.SWORDSMAN] == 0 and campaign.faction_units[faction.name][UnitType.CAVALRY] == 0:
                    self.campaigns.remove(campaign)  


    def init_openAI(self):
        path = os.path.dirname(os.path.abspath(__file__)).replace("/Modules","")
        if not os.environ.get("OPENAI_API_KEY") and not os.path.exists(f"{path}/API_Key.txt"):
            key = input("Please enter your OpenAI API key: ")
            os.environ["OPENAI_API_KEY"] = key
        elif os.path.exists(f"{path}/API_Key.txt"):
            with open(f"{path}/API_Key.txt") as f:
                os.environ["OPENAI_API_KEY"] = f.read()

        if not os.environ.get("ASSISTANT_ID") and not os.path.exists(f"{path}/assistant_id.txt"):
            key = input("Please enter the faction assistant id: ")
            os.environ["ASSISTANT_ID"] = key
        elif os.path.exists(f"{path}/assistant_id.txt"):
            with open(f"{path}/assistant_id.txt") as f:
                os.environ["ASSISTANT_ID"] = f.read()

        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.client = client
    

class Faction:
    def __init__(self, name: str, regions: list):
        self.name = name
        self.regions = regions
        self.units = [Archer(0), Swordsman(0), Cavalry(0)]
        self.fore_style_colors = [Fore.RED, Fore.GREEN, Fore.BLUE, Fore.YELLOW, Fore.MAGENTA, Fore.CYAN]
        self.fore_style_color = random.choice(self.fore_style_colors)
        self.thread_id = None

    def __repr__(self) -> str:
        return f"{self.fore_style_color}{self.name}{Style.RESET_ALL}"
    
    def get_faction_name(self) -> str:
        return self.name
    
    def get_faction_regions(self) -> list:
        return self.regions
    
    def get_faction_units(self) -> list:
        return self.units
    
    def get_faction_unit_counts(self):
        print(f"{self.fore_style_color}{self.name} has {self.units[0].count} archers, {self.units[1].count} swordsmen, {self.units[2].count} cavalry.{Style.RESET_ALL}")
        return f"{self.fore_style_color}{self.name} has {self.units[0].count} archers, {self.units[1].count} swordsmen, {self.units[2].count} cavalry.{Style.RESET_ALL}"

    def init_faction_assistant(self,client):
        thread = client.beta.threads.create()
        self.thread_id = thread.id

        
    
    def action_prompt_faction_assistant(self,content:str) -> str:     
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

        faction_message = client.beta.threads.messages.create(
            thread_id=self.thread_id,
            role="user",
            content=content
        )

        run = client.beta.threads.runs.create_and_poll(
            thread_id=self.thread_id,
            assistant_id=os.environ["ASSISTANT_ID"],
        )

        if run.status == 'completed':
            thread_messages = client.beta.threads.messages.list(
            thread_id=self.thread_id,
            order="desc",
            limit=1
            )
        faction_assistant_response = thread_messages.data[0].content[0].text.value
        return str(faction_assistant_response)
    
    def top_level_choices_prompt(self):
        return self.action_prompt_faction_assistant("""
**Choices**
1.Recruit units
2.Start/join attack campaign
3.Start/bolster defense campaign
4.Get current campaigns
5.Get owned regions
6.Get owned units
7.Get simulation info
""")
    
    def recruit_choices_prompt(self):
        return self.action_prompt_faction_assistant("""
Options:
1. archer
2. swordsman
3. cavalry
"""
        )

    def campaign_choices_prompt(self,attack_regions:list) -> str:
        return self.action_prompt_faction_assistant(f"{", ".join(attack_regions)} please select only a region from this list and return just the region name excluding anything in parentheses and the parentheses themselves.")
    
    def campaign_join_prompt(self,unit_type: UnitType):
        match unit_type:
            case UnitType.ARCHER:
                indx = 0
            case UnitType.SWORDSMAN:
                indx = 1
            case UnitType.CAVALRY:
                indx = 2
        return self.action_prompt_faction_assistant(f"How many {unit_type.name} should join the campaign? you have {self.units[indx]} {unit_type.name}s currently. Return only a number that is less than or equal to {self.units[indx]}")

    def tell_faction_assistant(self,message:str):
        self.action_prompt_faction_assistant(message)
    

class Region:
    def __init__(self, name: str, description: str, owner: Faction):
        self.name = name
        self.description = description
        self.owner = owner
        self.campaign = None
    
    def __repr__(self) -> str:
        return f"{self.owner.fore_style_color}{self.name} ({self.owner.name}){Style.RESET_ALL}"
    
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
        if count < 0:
            raise Exception("Cannot recruit negative units.")
        if count == 0:
            raise Exception("Cannot recruit 0 units.")
        self.count += count
    
    def remove_units(self, count: int) -> None:
        if count < 0:
            raise Exception("Cannot remove negative units.")
        if count > self.count:
            raise Exception("Cannot remove more units than are available.")
        self.count -= count
    

class Archer(Unit):
    def __init__(self,count):
        super().__init__(UnitType.ARCHER, 5, 3, 1, count)


class Swordsman(Unit):
    def __init__(self,count):
        super().__init__(UnitType.SWORDSMAN, 2, 7, 15, count)


class Cavalry(Unit):
    def __init__(self,count):
        super().__init__(UnitType.CAVALRY, 3, 7, 8, count)