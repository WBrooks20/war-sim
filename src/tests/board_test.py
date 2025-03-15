import unittest
import sys
import os

# Add the parent directory of 'Modules' to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from Modules.sim_objects import Board, Faction, Region,Actions
from Modules.actions import recruit_units_action

class TestBoard(unittest.TestCase):

    def test_init_board(self):
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

        self.assertEqual(new_board.regions, regions)
        self.assertEqual(new_board.factions, factions)
    
    def test_update_action_count(self):
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

        new_board.update_action_count(Actions.RECRUIT)

        self.assertEqual(new_board.faction_action_count, 2)

        new_board.update_action_count(Actions.RECRUIT)
        new_board.update_action_count(Actions.RECRUIT)
        self.assertEqual(new_board.faction_action_count, 3)


    


if __name__ == '__main__':
    unittest.main()