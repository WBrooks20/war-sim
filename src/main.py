from Modules.sim_objects import Board
from Modules.sim_objects import Faction
from Modules.sim_objects import Region
from Modules.actions import recruit_units_action

def main():
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

    # Testing the Board class
    new_board = Board()
    new_board.init_board(regions, factions, 1093)

    # Testing the Faction class
    print(new_board.regions[0].name)

if __name__ == "__main__":
    main()