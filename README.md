# Traveller-Sector-Generator
A work in progress Sector or Subsector generator for the classic Traveller RPG

This script outputs a text file containing sector data compatible with [Traveller Map's postermaker API](https://travellermap.com/make/poster).

The variable map_size at line 385 can be set to 'sector' to generate a full 32 x 40 map, or 'subsector to generate a smaller 8x10 map.

The variable system_presence at line 386 can be set to an interger between 1 and 6. This is the minimum value on a six-sided die that indicates a system is located in a given set of coordinates.
