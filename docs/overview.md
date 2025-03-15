## WarSim

### General overview

WarSim is an AI powered war simulator leveraging GPT-4. Given data values for specific units WarSim can simulate battles for those units and determine the victor. Battles are fought between armies of units and the army with remaining units after the simulaton win. Battles make up campaigns which in turn make up wars. Campaigns can have multiple battles and wars can have multiple campaigns. If a faction wins a war they win the region that war happened in. The ultimate goal of each faction is to take over every region on the map.

### Terminology

- Region: A region is an an area of land on the map. Regions can be won in wars. Owning a region will provide unique advantages to the faction.
- Faction: A faction is an organized group that owns armies and regions. They represent the player. Factions compete to take over regions by winning wars. 
- War: A war is made up of campaings. Winning a war grants the winning faction the region. 
- Campaign: A campain is a grouping of battles that span across a region. Winning the most campaigns results in winning the war. 
- Battle: A battle is fought between factions arimes of units and happen within campaigns. WarSim simlates the battle using factors from the battle environment and unit information. 
- Army: A collection of units that belong to a faction. Armies fight in battles to determine the winning faction.
- Unit: A single instance of a soldier within an army. Units can of be multiple types (for example calvery, archer, infantry ect.). Each unit type has unique strenghts and weaknesses. 
- Year: Every in game year each faction gets a turn. If there are 3 factions then the year will consist of 3 turns. 
- Phase: Each year makes up two phases. The Action phase goes first in which each player makes their 3 actions. The Battle phase goes second in which battles are simulated. Wars, campaigns and battles are fought and won in the battle phase. 
- Turn:  Action phases in WarSim happen in turns. Each year a faction gets a turn. On the factions turn they may commit actions to happen that year. 
- Actions: Actions are what a faction does durring their turn. Examples include starting a war on a region and creating units.
- Unit reserve: the amount of units a faction has. 

### Win condition

To win WarSim a faction must gain complete control over all of the regions on the map. 

### Losing condition

Any faction that runs out of regions loses the WarSim. 

### Rules

- Factions may take only 3 actions per turn. Possible actions are recruit units, declare war on a region, or defending a region. 
- Factions may not declare war on a region in which a war is already happening. 
- Factions may not declare war on a region they already own.
- Factions may only declare war on a region adjacent to a region they already own. 
- Factions may declare with with as many campaings as they wish. The defending faction can defend with as many campaings as they wish. Any campaings not defended against will automatically be a win for the attacking faction. 

### Play Flow

#### Start
- Every faction starts with x number of each unit and specific regions.

#### Action Phase
 
- Attacking: Attacking factions action: attacking faction decides how many campaings to dedicate to the attack. Attacking faction decides how many units to allocate to each campaign. 
- Defending: Defending factions action: defending faction decides how many campaings to dedicate to the defense. Defending faction decides how many units to allocate to each campaign. 
- Recruiting: The faction uses an action to recruit additional units. The amount of units recruited will depend on the type of unit and the region. 
#### Battle Phase

- A random number of battles are instanced for each campaign in each war. Factions decide what units to allocate to each battle from their campaign unit pool decided in the action phase. 
- Battles are run one by one in each campaign in each war.
- Battles are simulated based off of enviornmental factors as well as unit health, damage, armor ect values and regional benifits. 
- Each simulated battle results in a victor. 
- The faction that wins the most battles in a campaign wins the campaign. 
- The faction that wins the most campaigns in a war wins the war.
- The faction that wins the war is given the region. 
- After all battles, campaigns and wars are simulated WarSim switches back to the action phase as long as there are remaining factions. 

#### Limits
- 6 faction limit due to color options.
