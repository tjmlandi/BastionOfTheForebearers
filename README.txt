Team SoloMid : Bastion of the Forebearers

Names:
Thomas Landi
Aaron Starr
Lijing Zhang

Pre-Reqs:
- Have MySQL, using the workbench.
- Python 2.7

Installation:
- Have the username root with the password "password"
- Run CreateTables.py while having MySQL installed
- Run BotF.py to test login (you'll have to pull a user/pw from the database)

The database is in 1st normal form due to there being no "lists" within attribute columns. Every field holds one value and each value is within the domain.
t is not in 2nd normal form yet as this may not occur until the champion table is created and ranking updates are completed.