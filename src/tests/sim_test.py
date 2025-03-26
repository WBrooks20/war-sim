import unittest
import sys
import os
# Add the parent directory of 'Modules' to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from Modules.sim_objects import Board, Faction, Region, UnitType, Phase
from Modules.actions import recruit_units_action, attack_campaign_action, defense_campaign_action
from Modules.battle import battle
import random
from time import sleep

class TestCampaign(unittest.TestCase):

    def archers_swordsman_turn(self,new_board,regions):
        faction = new_board.faction_turn

        # Recruit units for the current faction's turn
        recruit_units_action(new_board.faction_turn, UnitType.ARCHER, new_board)

        recruit_units_action(new_board.faction_turn, UnitType.SWORDSMAN, new_board)
        
        last_action = random.randint(0,1)

        if (last_action == 0):
            # Attack campaign action
            attack_regions = regions.copy()
            for region in faction.regions:
                attack_regions.remove(region)
            attack_campaign_action(new_board, faction, random.choice(attack_regions), {UnitType.ARCHER: random.randint(0,faction.units[0].count), UnitType.SWORDSMAN: random.randint(0,faction.units[1].count), UnitType.CAVALRY: random.randint(0,faction.units[2].count)})
        
        else: 
            defense_campaign_action(new_board, faction, random.choice(faction.regions), {UnitType.ARCHER: random.randint(0,faction.units[0].count), UnitType.SWORDSMAN: random.randint(0,faction.units[1].count), UnitType.CAVALRY: random.randint(0,faction.units[2].count)})



    def archers_calvery_turn(self,new_board,regions):
        faction = new_board.faction_turn

        # Recruit units for the current faction's turn
        recruit_units_action(new_board.faction_turn, UnitType.ARCHER, new_board)

        recruit_units_action(new_board.faction_turn, UnitType.CAVALRY, new_board)

        last_action = random.randint(0,1)

        if (last_action == 0):
            # Attack campaign action
            attack_regions = regions.copy()
            for region in faction.regions:
                attack_regions.remove(region)
            attack_campaign_action(new_board, faction, random.choice(attack_regions), {UnitType.ARCHER: random.randint(0,faction.units[0].count), UnitType.SWORDSMAN: random.randint(0,faction.units[1].count), UnitType.CAVALRY: random.randint(0,faction.units[2].count)})
        
        else: 
            defense_campaign_action(new_board, faction, random.choice(faction.regions), {UnitType.ARCHER: random.randint(0,faction.units[0].count), UnitType.SWORDSMAN: random.randint(0,faction.units[1].count), UnitType.CAVALRY: random.randint(0,faction.units[2].count)})



    def swordsman_calvery_turn(self,new_board,regions):
        faction = new_board.faction_turn

        # Recruit units for the current faction's turn
        recruit_units_action(new_board.faction_turn, UnitType.CAVALRY, new_board)

        recruit_units_action(new_board.faction_turn, UnitType.SWORDSMAN, new_board)


        last_action = random.randint(0,1)

        if (last_action == 0):
            # Attack campaign action
            attack_regions = regions.copy()
            for region in faction.regions:
                attack_regions.remove(region)
            attack_campaign_action(new_board, faction, random.choice(attack_regions), {UnitType.ARCHER: random.randint(0,faction.units[0].count), UnitType.SWORDSMAN: random.randint(0,faction.units[1].count), UnitType.CAVALRY: random.randint(0,faction.units[2].count)})
        
        else: 
            defense_campaign_action(new_board, faction, random.choice(faction.regions), {UnitType.ARCHER: random.randint(0,faction.units[0].count), UnitType.SWORDSMAN: random.randint(0,faction.units[1].count), UnitType.CAVALRY: random.randint(0,faction.units[2].count)})
        

    def test_battle_phase(self):
        # Create factions
        knights = Faction("knights", [])
        indians = Faction("indians", [])
        tribals = Faction("tribals", [])
        factions = [knights, indians, tribals]

        # Create regions and assign them to factions
        suadia = Region("suadia", "desert", knights)
        england = Region("england", "green", knights)
        america = Region("america", "forest", indians)
        canada = Region("canada", "snow", indians)
        brazil = Region("brazil", "jungle", indians)
        india = Region("india", "desert", tribals)
        mexico = Region("mexico", "desert", tribals)
        argentina = Region("argentina", "desert", tribals)

        knights.regions = [suadia, england]
        indians.regions = [america, canada, brazil]
        tribals.regions = [india, mexico, argentina]
        regions = [suadia, england, america, canada, brazil, india, mexico, argentina]

        # Initialize the board
        new_board = Board()
        new_board.init_board(regions, factions, 1903)


        while (len(new_board.factions) >= 1):

            while new_board.current_phase == Phase.ACTION:
                new_board.remove_losing_factions()
                self.archers_swordsman_turn(new_board,regions)
                sleep(5)
                self.archers_calvery_turn(new_board,regions)
                sleep(5)
                self.swordsman_calvery_turn(new_board,regions)
                sleep(5)
            
            new_board.get_current_campaigns(new_board.faction_turn)
            for faction in new_board.factions:
                print(f"{faction} has {faction.units[0].count} archers, {faction.units[1].count} swordsmen, {faction.units[2].count} cavalry.")
                
            while new_board.current_phase == Phase.BATTLE:
                for campaign in new_board.campaigns:
                    battle(campaign,new_board)
                sleep(5)
                new_board.update_phase()

if __name__ == '__main__':
    unittest.main()