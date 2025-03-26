import unittest
import sys
import os

# Add the parent directory of 'Modules' to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src')))

from Modules.sim_objects import Board, Faction, Region, UnitType
from Modules.actions import recruit_units_action

class TestActions(unittest.TestCase):

    def test_recruit_action(self):
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
        recruit_units_action(new_board.faction_turn, UnitType.ARCHER, new_board)
        self.assertEqual(faction.units[0].count, 100)
        recruit_units_action(new_board.faction_turn, UnitType.ARCHER, new_board)
        self.assertEqual(faction.units[0].count, 150) # Turn switches to next faction.

        # Switch to the next faction's turn
        faction = new_board.faction_turn
        recruit_units_action(new_board.faction_turn, UnitType.SWORDSMAN, new_board)
        self.assertEqual(faction.units[1].count, 100)
        recruit_units_action(new_board.faction_turn, UnitType.SWORDSMAN, new_board)
        self.assertEqual(faction.units[1].count, 200)
        recruit_units_action(new_board.faction_turn, UnitType.SWORDSMAN, new_board)
        self.assertEqual(faction.units[1].count, 300) # Turn switches to next faction.

        # Switch to the next faction's turn
        faction = new_board.faction_turn
        recruit_units_action(new_board.faction_turn, UnitType.CAVALRY, new_board)
        self.assertEqual(faction.units[2].count, 30)
        recruit_units_action(new_board.faction_turn, UnitType.CAVALRY, new_board)
        self.assertEqual(faction.units[2].count, 60)
        recruit_units_action(new_board.faction_turn, UnitType.CAVALRY, new_board)
        self.assertEqual(faction.units[2].count, 90) # End of turns, start of battle phase. 

        # Print the units count for each faction
        for faction in new_board.factions:
            print(f"{faction} has {faction.units[0].count} archers, {faction.units[1].count} swordsmen, {faction.units[2].count} cavalry.")

if __name__ == '__main__':
    unittest.main()