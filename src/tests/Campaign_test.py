import unittest
import sys
import os

# Add the parent directory of 'Modules' to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from Modules.sim_objects import Board, Faction, Region, UnitType
from Modules.actions import recruit_units_action
from Modules.sim_battle_classes import Campaign

class TestCampaign(unittest.TestCase):

    def test_add_units_to_campaign(self):
        knights = Faction("knights", [])
        indians = Faction("indians", [])
        tribals = Faction("tribals", [])
        factions = [knights, indians, tribals]

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

        new_board = Board()
        new_board.init_board(regions, factions, 1903)
        faction = new_board.faction_turn
        recruit_units_action(new_board.faction_turn, UnitType.ARCHER, 10, new_board)
        self.assertEqual(faction.units[0].count, 10)
        recruit_units_action(new_board.faction_turn, UnitType.SWORDSMAN, 10, new_board)
        self.assertEqual(faction.units[0].count, 10)
        suadia_campaign = Campaign(new_board, suadia)
        suadia_campaign.add_faction_units(new_board.faction_turn, {UnitType.ARCHER: 10, UnitType.SWORDSMAN: 10})
        suadia_campaign.join_campaign(knights)
        suadia_campaign.add_faction_units(knights, {UnitType.ARCHER: 25, UnitType.SWORDSMAN: 25})
        suadia_campaign.get_faction_units()
        


if __name__ == '__main__':
    unittest.main()