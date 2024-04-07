# Kirby Super Star Randomizer

This is a randomizer for Kirby Super Star. This software currently only allows for room randomization in the Great Cave Offensive sub-game, but more features will soon be added.

# Setup

In order to use this randomizer, you will need the following:
- The randomizer software and a computer to run said software (to download the program .exe, click the Releases button on the right side of the page)
- A ROM of Kirby Super Star. This can be either English or Japanese 1.2, with support for more versions planned for the future.
- A way to play the ROM. This could be an emulator, flashcart, etc.

Launch the program, enter your ROM path and output path, select settings and generate the ROM.

Below is a list of what each option does. The software will have the recommended settings automatically selected, so feel free to just click generate if you aren't picky.

# Options
Seed: The RNG seed that the randomizer will use. If you want to play the same randomized map with others, everyone should set this number to the same number and you will all receive the exact same layout.

## Randomize Doors
### Randomization Options
- Two-Way Doors Only: Only shuffle doors that are bidirectional. One-way doors will not be altered.
- Shuffle By Type: Shuffle two-way doors and one-way doors separately.
- Total Random: Shuffle everything together.

### Shuffle Special Doors
- Randomize Save Doors: If checked, save doors will be added to the shuffler. Turn this off if you would rather have save doors be in their usual spots.
- Randomize Ability Rooms: If checked, ability rooms before boss fights will be shuffled. Turn this off if you would rather have ability rooms always be in front of boss doors.
  - Note: There is still the chance that you may approach a boss from its typical exit door, meaning that you will not enter the ability room until after the boss fight.
- Randomize Switch Puzzle: The switch puzzle doors refer to the third room in Subtree that has doors which reset you to the beginning of the puzzle if Kirby gets stuck. Turn this on if you would prefer to have these doors shuffled. However, this will make it so three randomly selected doors will lead you back to the beginning of the switch puzzle.

# Credits

- A huge thank you to TG and his [Amazing Mirror Randomizer](https://github.com/HeyImTG/Amazing-Mirror-Randomizer) for laying the foundation for this one. The KSS randomizer borrows from his randomizer UI, and the door randomization algorithm is also heavily inspired by his own.
- Thank you to the Mesen emulator for making data collection a lot less tedious using its debugger.
- Thank you to zzzhonki for help with the Japanese UI translation.
- Thank YOU for your interest in this randomizer. I hope you enjoy :)
