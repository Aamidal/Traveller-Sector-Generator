# markov-name-generator
A Markov chain-based name generator, currently a work in progress intended to provide fictional place names inspirated by real world city names.

Reads names from 'inspiration.txt' and generates new names like them. 

User can keep or reject the output. Rejected names are saved to 'reject.txt',
and will not be output again.

Kept names are saved in 'keep.txt' and will also be seeded back into the pool
the generator operates from. 

## Utilities
Data directory contains open source datasets with city names and international
people names.

Use name_extractor.py to extract names from worldcities.csv.
strip.py was used to clean up a list from an earlier version of this project.
