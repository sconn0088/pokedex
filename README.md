# pokedex
INTRODUCTION

What if Pokémon were real?

That was the original concept that initiated this project. I've been a fan of the game since I first played it as a nine-year-old kid. In the game of Pokémon, you battle opponents with your selected pocket monsters until you finally ascend to the top of the Pokémon League and become the best trainer in the world.

So how do you get to the apex? Sure, you could level up your Pokémon team until you can just bulldoze every opponent. That might be a viable strategy in the game. But we're not talking about the game here. We're talking about real life. And in real life your opponent isn't going to sit back at level 12, or level 25, or even level 50 while you grow to level 80, 90, or 100. Your opponent is going to be leveling up right there with you. In order to gain that edge, you need a real-life Pokédex.

THE POKÉDEX

That's where this project comes in. I created a real-life Pokédex that can calculate your win percentage against any opponent.

Here's how it works: First, you select your Pokémon and your Pokémon's level. All original 151 Pokémon are included for selection and the levels range from 2 to 100.

Next, you select what Pokémon your opponent will use in battle and also what level your opponent's Pokémon is. Each Pokémon can know up to four moves at any time, so the next step is to select which four moves you want for your Pokémon; ditto for your opponent.

Finally, once the combatants are selected, the Pokémon enter the battle area and fight one thousand times, after which the Pokédex will calcualte your win percentage for you out of 100%.

DEPARTURES FROM THE GAME

Moves:
I included 163 out of 164 possible moves from the game. The only move that is omitted is Struggle. In the game, you can only use a specific move a certain number of times per battle. This is known as the move's PP.

Basic moves, such as Tackle, have a high PP number (35) while more powerful moves, such as Fire Blast, have a much lower number (5). Once you run out of PP for a specific move, you cannot use that move again for the rest of the battle. If you run out of PP for all possible moves, you get to use a unique move called Struggle, which deals damage to the enemy while simultaneously inflicting damage on yourself. I did not include Struggle in the program because the concept of PP is ignored entirely.

Levels:
You can pick any of the 151 Pokémon and choose any level between 2 and 100. While Pokémon in the game have to be a certain level in order to learn specific moves, I ignored that restriction. As long as the Pokémon is able to learn a certain move at any point, you can select to use that move regardless of level.

For example, Charizard does not learn Flamethrower until level 46. However, if you select Charizard as your fighter and you select a level below 46, Flamethrower remains a viable move option.

Evolutions: In the game, certain Pokémon only evolve with stones. After evolving with said stone, they usually cannot learn new moves naturally. This evolutionary concept is ignored. If a move is reserved for a specific evolution, however, that concept is still upheld.

Example 1: Raichu evolves from Pikachu with a thunder stone. Once evolved, Raichu cannot learn any new moves. In order for Raichu to be able to use the move Thunder, it has to learn Thunder as Pikachu before using the thunder stone to evolve into Raichu. That mechanic is ignored. If you select Raichu as your Pokémon, it can use Thunder as one of its moves regardless of level.

Example 2: Caterpie has a three Pokémon evolution chain: Caterpie evolves into Metapod which in turn evolves into Buterfree. In the game, if you catch a wild Butterfree that did not evolve from Metapod, that Butterfree cannot learn the move Harden. This concept is ignored. Because Butterfree evolves from Metapod and Caterpie, Butterfree can select to use any move that is available to either Caterpie or Metapod.

Example 3: Nidoking evolves from Nidorino using a moon stone. If evolved early enough in the game, Nidoking can learn Thrash at level 23. Nidorino can never learn Thrash. This concept is upheld, and the move Thrash is not a selectable move for Nidorino. Any move that is learned by Nidorino, by contrast, is selectable for Nidoking.

MECHANICS

The battle engine is written in python. The data for the Pokémon and the moves is stored in a database using MySQL.
