from Modules.sim_objects import Board
from Modules.sim_objects import Faction
from Modules.sim_objects import Region
from Modules.sim_objects import UnitType,Actions
from colorama import Fore, Back, Style

def recruit_units_action(faction: Faction, unit: UnitType, count: int, board: Board) -> None:
    try: 
        board.update_action_count(Actions.RECRUIT)
    except Exception as e:
        print(e)
        return
    print(f"{faction.fore_style_color}Recruiting {count} {unit.name} units for {faction}{Style.RESET_ALL}")

    for current_unit in faction.units:
        if current_unit.name == unit:
            current_unit.recruit_units(count)
            print(f"{faction.fore_style_color}{current_unit}{Style.RESET_ALL}")
            return
    raise Exception(f"Invalid unit type: {unit}")

