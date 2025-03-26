from Modules.sim_objects import Board
from Modules.sim_objects import Faction
from Modules.sim_objects import Region
from Modules.sim_objects import UnitType,Actions, CampaignType
from Modules.sim_battle_objects import Campaign

from colorama import Fore, Back, Style

def recruit_units_action(faction: Faction, unit: UnitType, board: Board) -> None:

    match unit:
        case UnitType.ARCHER:
            count = 50
        case UnitType.SWORDSMAN:
            count = 100
        case UnitType.CAVALRY:
            count = 30
        case _:
            raise Exception(f"Invalid unit type: {unit}")
        
    print(f"{faction.fore_style_color}Recruiting {count} {unit.name} units for {faction}{Style.RESET_ALL}")

    for current_unit in faction.units:
        if current_unit.name == unit:
            current_unit.recruit_units(count)
            print(f"{faction.fore_style_color}{current_unit}{Style.RESET_ALL}")
            try: 
                board.update_action_count(Actions.RECRUIT)
            except Exception as e:
                print(e)
            return
    raise Exception(f"Invalid unit type: {unit}")


def attack_campaign_action(board: Board, faction: Faction, region: Region, units: dict) -> None:
    if region  in faction.regions: 
        raise Exception (f"{faction} owns {region}. Factions cannot start an attack campaign on regions they own.")

    if region.campaign is None:
        region.campaign = Campaign(board, region, CampaignType.Attack)
        print(f"{faction} has started an attack campaign on {region}{Style.RESET_ALL}")
        region.campaign.join_campaign(faction)
        board.campaigns.append(region.campaign)
    else: 
        region.campaign.join_campaign(faction)
        print(f"{faction} has joined the attack campaign on {region}{Style.RESET_ALL}")
    
    campaign = region.campaign
    try:
        campaign.add_faction_units(faction, units)
        campaign.get_faction_units()
        board.update_action_count(Actions.ATTACK)
    except Exception as e:
        print(e)
        return
    

def defense_campaign_action(board: Board, faction: Faction, region: Region, units: dict) -> None:
    if region not in faction.regions: 
        raise Exception (f"{faction} does not own {region}. Factions can only start a defense campaign on regions they own.")

    if region.campaign is None:
        region.campaign = Campaign(board, region,CampaignType.Defend)
        print(f"{faction} has started a defense campaign on {region}{Style.RESET_ALL}")
        region.campaign.join_campaign(faction)
        board.campaigns.append(region.campaign)
    elif faction not in region.campaign.factions:
        region.campaign.join_campaign(faction)
        print(f"{faction} has joined the defense campaign on {region}{Style.RESET_ALL}")
    
    campaign = region.campaign
    try:
        campaign.add_faction_units(faction, units)
        campaign.get_faction_units()
        board.update_action_count(Actions.DEFEND)
    except Exception as e:
        print(e)
        return
    
