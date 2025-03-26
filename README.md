## WarSim

### General Overview

WarSim is an AI-powered war simulator leveraging GPT-4. WarSim takes place in two phases: the action phase and the battle phase. During the action phase, each faction takes a turn consisting of three actions. Possible actions are: Recruit to recruit new units and add them to the faction's unit reserve; start/join an attack campaign to start a new or join an existing attack campaign on a region; and start/bolster a defense campaign to start a defense campaign on an owned region or bolster an existing defense campaign with additional units. During the battle phase, each campaign undergoes a battle to determine who gets the region the campaign was started in. The battle simulates each faction's units attacking in turns. At the end of the battle, the faction with remaining units wins and becomes the owner of the region. If the campaign was an attack campaign, it is converted to a defense campaign containing the winning faction's remaining units in that campaign. After the battle phase, the sim switches the phase back to action, and each remaining faction takes a turn of 3 actions. If a faction has 0 remaining regions, the faction is dropped from the game. The goal is to be the only faction remaining.

### Terminology

- **Region**: A region is an area of land on the map. Regions can be won in battles. Owning a region provides unique advantages to the faction.
- **Faction**: A faction is an organized group that owns armies and regions. They represent the player. Factions compete to take over regions by winning battles.  
- **Campaign**: A campaign is a grouping of units for each faction in a region. Campaigns can be one of two types: an attack campaign or a defense campaign. A campaign is of type attack if a faction that does not own a region starts an attack campaign on the region AND the region does not currently have a defense campaign to meet the attacking faction's forces. A campaign is of type defense if the owner of the region begins a defense campaign on the region, or if the region was won by the owner in a previous battle and the owner had remaining units after the battle. In this case, the campaign is converted to a defense campaign and the winning faction's units are left in the campaign to defend the region. Attackers can join a defense campaign as an opposing force to attempt to take over the region.  
- **Battle**: A battle is fought between factions' armies of units and happens within campaigns. WarSim simulates the battle using factors from the battle environment and unit information. 
- **Army**: A collection of units that belong to a faction. Armies fight in battles to determine the winning faction and reside in campaigns. 
- **Unit**: A single instance of a soldier within an army. Units can either be archers, swordsmen, or cavalry. Each unit type has unique strengths and weaknesses. 
- **Year**: A year is a single action phase and battle phase.
- **Phase**: Each year is made up of two phases. The Action phase goes first, in which each faction makes their 3 actions. The Battle phase goes second, in which battles are simulated.
- **Turn**: Action phases in WarSim happen in turns. Each year, a faction gets a turn. On the faction's turn, they may commit actions to happen that year. 
- **Actions**: Actions are what a faction does during their turn. Examples include starting a campaign on a region or recruiting units.
- **Unit Reserve**: The amount of units a faction has. 

### Win Condition

To win WarSim, a faction must gain complete control over all of the regions on the map. 

### Losing Condition

Any faction that runs out of regions loses the WarSim. 

### Rules

- Factions may take only 3 actions per turn.
- Factions may only start/join an attack campaign on a region once per turn. They may start/join attack campaigns on a different region each turn if they so choose. 
- Factions may start/bolster a defense campaign on a single region more than once in a turn. 
- Factions may not declare war on a region they already own.
- Any campaign with only one faction will result in that faction winning in the battle phase. 
- If a faction wins either an attack campaign or a defense campaign (an attacking faction defeating a defending faction's forces in a campaign or a defending faction successfully defending against an attack campaign by contributing forces of their own to the attack campaign on their turn), the campaign is converted to a defense campaign and the winning faction's forces for that campaign remain to defend the region in the defense campaign.
- An attack campaign can only actually occur if there is not an existing defense campaign on the region. If a defense campaign already exists, the attacking forces join the defense campaign to battle the existing defenders in the battle phase. 
- If a defense campaign has 0 of each unit type, it will be removed, and an attack campaign or a new defense campaign can start on that region.  

### Play Flow

#### Start
- Every faction starts with 0 of each unit and specific regions.
- A faction is chosen to be the first player in the action phase. 

#### Action Phase
- Any factions with 0 regions are removed from the sim. 
- Each faction gets 3 actions per turn. In those 3 actions, they can choose one of three actions to take: Recruit to recruit new units, Start/join attack campaign to start an attack campaign, join an existing attack campaign started by another faction, or join a defense campaign started by another faction in an attempt to take over that region, and start/bolster a defense campaign to start a new defense campaign on an existing region or bolster existing forces on an existing defense campaign. 
- At the end of the action phase, the phase shifts to the battle phase. 

#### Battle Phase

- For each ongoing campaign, a battle happens. 
- For defense campaigns in which no one else joins, nothing happens and the campaign stays as it was. 
- For attack campaigns in which only one faction joins, that faction wins the region. 
- After the battle phase, the phase shifts back to the action phase. 

### Limits
- 6 faction limit due to color options.