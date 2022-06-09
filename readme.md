# Overview

Script for general parsing for class assignment. Mainly made for Fun Fun Saturday class assignment, but modular enough for anytype of limited assignment. User is responsible for the exact strategy of allocation (greedy allocation predefined), function mappings from their own data to specified fields, and participant/class data (in JSON).

ORIGINAL MOTIVE: Since forever, our volunteer organization has assigned classes to students by hand, which is error prone and time consuming. In order to maintain data integrity and our sanities, I hope to automate our approach to class assignment. Since I had time, I decided to make the code not spaghetti. Enjoy!

## Instructions

### 1. Procure your data

Classes data - ```data/classes.json```
Response data - ```data/responses.json```

### 2. Define the mapping and employ it

Define a class within ```mappers.py```, and use it in ```__main__.py```

### 3. Run the script

In root directory, run ```python3 __main__.py```

And there you go! Your sheets should be generated within the ```output``` directory, where there is a sheet for every class and an overall master sheet. They will be in the form of csv files.

## Timeline

1. Get 'hard coded' responses parsed and assigned classes to motivate general approach (1-2 days) (DONE! in archive folder)

2. Write reusable scripts for subsequent years (2 days) (DONE!)

3. Incorporate into concurrent modernization of UEAA Fun Fun data collection (1 month, not including the time for this S E C R E T project)
