from Modules.sim_objects import Board,Faction,Region,UnitType,Phase
from Modules.actions import recruit_units_action,defense_campaign_action,attack_campaign_action
from Modules.battle import battle
def main():
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
    play_board = Board()
    play_board.init_board(regions, factions, 1903)
    play_board.remove_losing_factions()
    play_board.init_openAI()

    for faction in factions:
        if not faction.thread_id:
            faction.init_faction_assistant(play_board.client)
            faction.tell_faction_assistant(f"Your faction is{faction.name}")
            print(f"{faction} GPT Initilized with thread id: {faction.thread_id}")

    while (len(play_board.factions) >= 1):
    # Start of action phase
        while play_board.current_phase == Phase.ACTION:
            play_board.remove_losing_factions()
            current_faction = play_board.faction_turn
            print(f"{current_faction} turn\n-----------------------------------\n")
            print("Eligible actions:\n1. recruit\n2. start/join attack campaign\n3. start/bolster defense campaign\n4. get current campaigns\n5. Get owned regions\n6. get owned units\n---------------------\nGPT response:")
            current_action = current_faction.top_level_choices_prompt()
            print(f"Current Action: {current_action}")

            if current_action == "1":
                print("\n Options:\n1. archer\n2. swordsman\n3. cavalry\nGPT response: ")
                unit = current_faction.recruit_choices_prompt()
                match unit:
                    case "1":
                        recruit_units_action(current_faction, UnitType.ARCHER, play_board)
                    case "2":
                        recruit_units_action(current_faction, UnitType.SWORDSMAN, play_board)
                    case "3":
                        recruit_units_action(current_faction, UnitType.CAVALRY, play_board)
                    case _:
                        print("Invalid unit type. Valid types are archer, swordsman, and cavalry.")
            
            elif current_action == "2":
                attack_regions = play_board.regions.copy()
                attack_region_names = []
                for region in current_faction.regions:
                    attack_regions.remove(region)
                print (f"\nRegions you can attack right now\n+++++++++++++++++++++++++++++++++++")
                for region in attack_regions:
                    print(region)
                    attack_region_names.append(region.name)
                attack_region = current_faction.campaign_choices_prompt(attack_region_names)
                attack_region = attack_region.lower()
                for region in play_board.regions:
                    if attack_region == region.name:
                        attack_region = region
                if isinstance(attack_region, Region): 
                    current_faction.get_faction_unit_counts()
                    try:
                        attack_number_of_archers = int(current_faction.campaign_join_prompt(UnitType.ARCHER))
                        attack_number_of_swordsman = int(current_faction.campaign_join_prompt(UnitType.SWORDSMAN))
                        attack_number_of_cavalry = int(current_faction.campaign_join_prompt(UnitType.CAVALRY))
                        print("-----------------------------------")
                        if (attack_number_of_archers > current_faction.units[0].count or attack_number_of_swordsman > current_faction.units[1].count or attack_number_of_cavalry > current_faction.units[2].count):
                            print("You cannot add more units than you have.")
                            continue
                        attack_campaign_action(play_board, current_faction, attack_region, {UnitType.ARCHER: attack_number_of_archers, UnitType.SWORDSMAN: attack_number_of_swordsman, UnitType.CAVALRY: attack_number_of_cavalry})
                    except Exception as e:
                        error_message = str(e)
                        if "invalid literal for int()" in error_message:
                            print("your selection must be a number.")
                        else:
                            print(e)
                else: 
                    print("This is not a valid region for an attack campaign.")
                    continue

            elif current_action == "3":
                defense_regions = current_faction.regions.copy()
                defense_region_names = []
                print (f"Regions you can defend right now\n")
                for region in defense_regions:
                    defense_region_names.append(region.name)
                    print(region)
                defense_region = current_faction.campaign_choices_prompt(defense_region_names)
                defense_region = defense_region.lower()
                for region in defense_regions:
                    if defense_region == region.name:
                        defense_region = region
                if isinstance(defense_region, Region): 
                    current_faction.get_faction_unit_counts()
                    try:
                        attack_number_of_archers = int(current_faction.campaign_join_prompt(UnitType.ARCHER))
                        attack_number_of_swordsman = int(current_faction.campaign_join_prompt(UnitType.SWORDSMAN))
                        attack_number_of_cavalry = int(current_faction.campaign_join_prompt(UnitType.CAVALRY))
                        if (attack_number_of_archers > current_faction.units[0].count or attack_number_of_swordsman > current_faction.units[1].count or attack_number_of_cavalry > current_faction.units[2].count):
                            print("You cannot add more units than you have.")
                            continue

                        defense_campaign_action(play_board, current_faction, defense_region, {UnitType.ARCHER: attack_number_of_archers, UnitType.SWORDSMAN: attack_number_of_swordsman, UnitType.CAVALRY: attack_number_of_cavalry})

                    except Exception as e:
                        error_message = str(e)
                        if "invalid literal for int()" in error_message:
                            print("your selection must be a number.")
                        else:
                            print(e)
                else: 
                    print("This is not a valid region for a defense campaign.")
                    continue

            elif current_action == "4":
                print("GPT Wants to see the current campaigns!")
                play_board.get_current_campaigns(current_faction)

            elif current_action == "5":
                print("GPT wants to see its current regions!")
                region_names = []
                for region in regions:
                    region_names.append(region.name)
                current_faction.tell_faction_assistant(", ".join(region_names))
                print("------------------------------")

            elif current_action == "6":
                print("GPT wants to see its current unit counts!")
                current_faction.tell_faction_assistant(current_faction.get_faction_unit_counts())

    # Start of the battle phase
        while play_board.current_phase == Phase.BATTLE:
            for campaign in play_board.campaigns:
                battle(campaign,play_board)
            play_board.update_phase()

if __name__ == "__main__":
    main()