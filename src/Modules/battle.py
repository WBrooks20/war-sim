from Modules.sim_objects import Board, Phase, Archer, Swordsman, Cavalry, CampaignType
from Modules.sim_objects import Faction
from Modules.sim_objects import UnitType
from Modules.sim_battle_objects import Campaign
import random

def battle_instance(campaign: Campaign, attacking_faction:Faction, defending_faction:Faction, attacking_units, defending_units):

    if (attacking_units.count <= 0):
        return 
    if (defending_units.count <= 0):
        return 
    
    print(f"{attacking_faction}: {attacking_units.count} {attacking_units.name.name} attacing {defending_faction}: {defending_units.count} {defending_units.name.name}")
    #Defending faction units are attacked first.
    defending_faction_remaining_units = attack(attacking_units, defending_units)
    campaign.faction_units[defending_faction.name][defending_units.name] = defending_faction_remaining_units

    # Check if the defending faction has any remaining swordsman
    if defending_faction_remaining_units > 0:
        # Defending faction retaliates
        print (f"{defending_faction} retaliates with {defending_faction_remaining_units} {defending_units.name.name} on {attacking_faction}'s {attacking_units.name.name} {attacking_units.count}")
        attacking_faction_remaining_units = attack(defending_units, attacking_units)
        campaign.faction_units[attacking_faction.name][attacking_units.name] = attacking_faction_remaining_units

    print(f"{attacking_faction} {attacking_units.name.name} remaining in this campaign: {campaign.faction_units[attacking_faction.name][attacking_units.name]}")
    print(f"{defending_faction} {defending_units.name.name} remaining in this campaign: {campaign.faction_units[defending_faction.name][defending_units.name]}")
    print("-------------------------------------------------")




def attack(attacker, defender):
    # Calculate the total damage dealt by the attacker
    total_damage = attacker.damage * attacker.count
    
    # Calculate the total health of the defender
    total_health = defender.health * defender.count
    
    # Calculate the remaining health after the attack
    remaining_health = total_health - total_damage
    
    # Calculate the remaining unit count of the defender
    remaining_units = max(0, remaining_health // defender.health)
    
    return int(remaining_units)

def battle(campaign: Campaign, board: Board):
    if board.current_phase != Phase.BATTLE:
        raise Exception(f"The current phase is {board.current_phase.name}. For a battle to start the phase must be {Phase.BATTLE.name}")
    if not campaign:
        raise Exception(f"No campaign selected for this battle.")
    if len(campaign.factions) == 1 and campaign.region in campaign.factions[0].regions and campaign.campaign_type == CampaignType.Defend:
        return
    if len(campaign.factions) == 1 and campaign.region not in campaign.factions[0].regions:
        campaign.factions[0].regions.append(campaign.region)
        campaign.region.owner.regions.remove(campaign.region)
        campaign.campaign_type = CampaignType.Defend
        campaign.region.owner = campaign.factions[0]
        print(f"{campaign.factions[0]} Wins the campaign on {campaign.region} by default as no factions joined the attack campaign.\n----------------------")
        return
    
    print(f"campaign region: {campaign.region}\n----------------------")
    while len(campaign.factions) > 1:
        #Keep a total unit count. 
        for current_faction in campaign.factions:
            #If the faction has no remaining units remove them from the campaign and continue. 
            current_faction_archers = int(campaign.faction_units[current_faction.name][UnitType.ARCHER])
            current_faction_swordsmen = int(campaign.faction_units[current_faction.name][UnitType.SWORDSMAN])
            current_faction_cavalry = int(campaign.faction_units[current_faction.name][UnitType.CAVALRY])
            if(current_faction_archers + current_faction_swordsmen + current_faction_cavalry <= 0):
                print(f"{current_faction} has no remaining units and is removed from the campaign.")
                campaign.faction_units.pop(current_faction.name)
                campaign.factions.remove(current_faction)
                continue

            # Determine possible factions to attack
            possible_factions_to_attack = campaign.factions.copy()
            possible_factions_to_attack.remove(current_faction)
            faction_to_attack = random.choice(possible_factions_to_attack)
            print(f"Faction turn: {current_faction}\nPossible Factions to attack: {possible_factions_to_attack}\nFaction to attack: {faction_to_attack}")

            current_unit_type = UnitType.ARCHER
            if  campaign.faction_units[current_faction.name][current_unit_type] > 0:

                #Archer order of attack: Swordsman, Archer, Cavalry
                current_faction_units = Archer(campaign.faction_units[current_faction.name][current_unit_type])
                defending_faction_units = Swordsman(campaign.faction_units[faction_to_attack.name][UnitType.SWORDSMAN])
                battle_instance(campaign, current_faction, faction_to_attack, current_faction_units, defending_faction_units)

                current_faction_units = Archer(campaign.faction_units[current_faction.name][current_unit_type])
                defending_faction_units = Archer(campaign.faction_units[faction_to_attack.name][UnitType.ARCHER])
                battle_instance(campaign, current_faction, faction_to_attack, current_faction_units, defending_faction_units)

                current_faction_units = Archer(campaign.faction_units[current_faction.name][current_unit_type])
                defending_faction_units = Cavalry(campaign.faction_units[faction_to_attack.name][UnitType.CAVALRY])
                battle_instance(campaign, faction_to_attack, current_faction, defending_faction_units, current_faction_units)

            current_unit_type = UnitType.SWORDSMAN
            if  campaign.faction_units[current_faction.name][current_unit_type] > 0:

                #Swordsman order of attack: Calvery, Swordsman, Archers
                current_faction_units = Swordsman(campaign.faction_units[current_faction.name][current_unit_type])
                defending_faction_units = Swordsman(campaign.faction_units[faction_to_attack.name][UnitType.SWORDSMAN])
                battle_instance(campaign, current_faction, faction_to_attack, current_faction_units, defending_faction_units)

                current_faction_units = Swordsman(campaign.faction_units[current_faction.name][current_unit_type])
                defending_faction_units = Archer(campaign.faction_units[faction_to_attack.name][UnitType.ARCHER])
                battle_instance(campaign, faction_to_attack, current_faction, defending_faction_units, current_faction_units)

                current_faction_units = Swordsman(campaign.faction_units[current_faction.name][current_unit_type])
                defending_faction_units = Cavalry(campaign.faction_units[faction_to_attack.name][UnitType.CAVALRY])
                battle_instance(campaign, current_faction, faction_to_attack, current_faction_units, defending_faction_units)

            current_unit_type = UnitType.CAVALRY
            if  campaign.faction_units[current_faction.name][current_unit_type] > 0:

                #Archer order of attack: Archers, Calvery, Swordsman
                current_faction_units = Cavalry(campaign.faction_units[current_faction.name][current_unit_type])
                defending_faction_units = Swordsman(campaign.faction_units[faction_to_attack.name][UnitType.SWORDSMAN])
                battle_instance(campaign, faction_to_attack, current_faction, defending_faction_units, current_faction_units)

                current_faction_units = Cavalry(campaign.faction_units[current_faction.name][current_unit_type])
                defending_faction_units = Archer(campaign.faction_units[faction_to_attack.name][UnitType.ARCHER])
                battle_instance(campaign, current_faction, faction_to_attack, current_faction_units, defending_faction_units)

                current_faction_units = Cavalry(campaign.faction_units[current_faction.name][current_unit_type])
                defending_faction_units = Cavalry(campaign.faction_units[faction_to_attack.name][UnitType.CAVALRY])
                battle_instance(campaign, current_faction, faction_to_attack, current_faction_units, defending_faction_units)

 
    if(len(campaign.factions) < 1):
        raise Exception(f"No one won the campaign on {campaign.region}.")
    
    if campaign.region not in campaign.factions[0].regions:
        campaign.factions[0].regions.append(campaign.region)
        campaign.region.owner.regions.remove(campaign.region)
        campaign.campaign_type = CampaignType.Defend

    campaign.region.owner = campaign.factions[0]
    print(f"{campaign.factions[0]} won the campaign on {campaign.region}!\n----------------------")












