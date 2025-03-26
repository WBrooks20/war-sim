import unittest
import sys
import os

# Add the parent directory of 'Modules' to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from Modules.sim_objects import Board, Faction, Region, UnitType
from Modules.actions import recruit_units_action, attack_campaign_action, defense_campaign_action
from Modules.sim_battle_objects import Campaign
import random

class TestCampaign(unittest.TestCase):

    def test_add_units_to_campaign(self):
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

        # Start of first faction turn
        faction = new_board.faction_turn

        # Recruit units for the current faction's turn
        recruit_units_action(new_board.faction_turn, UnitType.ARCHER, new_board)
        self.assertEqual(faction.units[0].count, 50)

        # Attack campaign action
        attack_regions = regions.copy()
        for region in faction.regions:
            attack_regions.remove(region)
        attack_campaign_action(new_board, faction, random.choice(attack_regions), {UnitType.ARCHER: 30})

        # Defense campaign action
        defense_campaign_action(new_board,faction, random.choice(faction.regions), {UnitType.ARCHER: 10})

        # Print the units count for each faction
        for faction in new_board.factions:
            print(f"{faction} has {faction.units[0].count} archers, {faction.units[1].count} swordsmen, {faction.units[2].count} cavalry.")

if __name__ == '__main__':
    unittest.main()