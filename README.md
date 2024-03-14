# Introduction

## Game Summary
	You, an intrepid adventurer was captured by THE WIZARD. You have no idea how long you have been in this forced sleep state. You were a statue in one of THE WIZARD's studies. You were there, you could see, could hear. But you weren't there either. For some reason you don't know why or how, you were waken up from your "sleep".
	Now your find yourself inside a tower and have absolutely no idea what to expect. Puzzles, enemies, diaries and even some messages from other adventurers that managed to escape (or tried!) can be found. Will you be able to escape? And what is THE MAGE doing anyway?
	You didn't escape? Well. Maybe the NEXT adventurer might do it...?
## Player Experience
	The player will explore a procedurally generated dungeon by reading descriptions of rooms and objects inside this dungeons. They will be able to chosen where to go, grab some itens, fight enemies, solve puzzles. The game will include sound (when the player can't see) and visual cues to help the player (a map of the dungeon).
## Platform
	PC
## Development Software
	VS Code (Python to generate Dungeon)
	Twine to Game
	Music from free assets
## Genre
	Single player, Puzzle Game
# Concept
## Overview
	The player controls a character that seeks to get out of a procedure generated dungeon (wizard tower). To do this it needs to look for the exit and solves puzzles. Sometimes the player will not be able to leave the tower, but hopefully will be rewarded with information that will help on next runs or information that helps understand the game's story. 

## Primary Mechanics

| **Name** | **Description** | 
| :--: | :--: |
| KeysLocks | Some doors need keys to be opened. There are two types of keys:<br>**Keys:** Literally keys, or orbs that need to be put at someplace to open the door<br>**Passwords:** Doors that required a password to be entered into.<br>**Conditions:** Some doors require the player is invisible or has drunk the super strength to go through.   | 
| Potions | Potions have different effects, these effects will be calculated upon a given seed that is set before the dungeon is generated. Determining the effects of a potion is a puzzle itself. | 
| Enemies | Enemies can be killed by paying an HP cost. If the player has an weapon, they can use the weapon to make this cost 0. | 
| Traps | Traps are activated when players enter a room. They reduce the player's HP in a certain amount. | 

## Specific Mechanics

#### Doors
| **Name** | **Description** |
| :--: | :--: |
| Wooden door | Wooden doors don't require keys. |
| Portal | Portals don't require keys. |
| Marble Arc | Marble arcs require an orb so that the portal is activated and the player goes through. |
| Metal door | Metal doors require keys to be opened. |
| Statue portal | Statue portals require that the player is invisible to go through the portal. If the player isn't, game over. |
| Weak walls | Weak Walls require the player has drunk the super strength potion to go through. |

#### Potions
Potions have a color and an number to their description.

Ex:. " A flask with a bright yellow liquid inside. In one of the sides there's a paper with handwritten numbers on it: [7750]"

These numbers represent what the potion does. The player may find tips about them throughout the tower. 

Based on a seed, rules that relate numbers to effects are generated.

Ex:. 
-> Potions with numbers divided by 5 reduced the players HP.
-> Potions with prime numbers grants invisibility.

The idea is to generate these rules and seed-base them. When the seed is changed, the rules are changed too.

#### Enemies / Weapons
Enemies are animals/monsters with a paired adjective that are divided in classes. 

Ex:. " A funny zombie rises up and starts walking towards you. "

The player eliminates the monster by paying an HP cost. If the player has the weapon that represents the weakness of that monster, it may not pay any HP cost. 

Each weapon will have a limited number of uses.

Ex:.
-> Silver arrows eliminate vampires without HP costs.
-> Lances eliminate Goblins without HP costs. And so on.

#### Traps
Traps are activated when the player walks into a room. The player gets its HP reduced.

#### Brainstorm
-> Have the player chose an item in the beginning of the run.
-> Have an item that gives tips on what's ahead.
-> Have a crafting table that allows the player to build potions with resources.

# Development Timeline

