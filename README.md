## CKLengds-Leveling
This project was developped at first by Hylted_ (Hylted_#6778 on Discord).
It was maded for having a leveling system on the guild "CK Legends"

## Run
Please install (Python)[https://python.org], `discord.py` library and `sqlite3` library.
You can install a library by doing the following command,
If you are on Windows, use `pip install <library name>`, for example `pip install discord.py`
If you aren't on Windows, use `python3 -m pip install <library name>`, for example `python3 -m pip install discord.py`
This bot was ONLY tested on Linux systems.

After you installed them all, please go in the directory where is the program with cd command and use, if you are on Windows, `python main.py`, or if you aren't, use `python3 main.py`
Please make sure you are in the right directory, you still can run that program for another directory, but the database will be saved on the directory you are in.

## Support
I offer a free support for that project, please contact me on Discord with my tag, Hylted_#6778
I'm actually on these Discord servers:
- (Aide Discord)[https://discord.gg/TFHuDr3JB3]
- (Protect ©| SUPPORT)[https://discord.gg/KKZfEtrWB7]
- (Tome & Code | Développeur)[https://discord.gg/6Vvy7TdUyh]

## Commands
### levels
> It returns XP for a specified user.
Usage: `levels <mention of user>`
Example of usage: `--levels @UserMention`
Aliases: `xp`, `niveaux`, `niveau`, `level`

### Shop
> It permits anyone to buys something
Usage: `shop <id>`
Example of usage: `--shop 8`
Aliases: `purchase`, `buy`, `store`

### Stop (admin only)
> It stops the bot if not started with the start.py script.
Usage: `stop`
Example of usage: `--stop`
Aliases: `admin-stop`, `adminstop`, `stopadmin`, `stop-admin`, `shutdown`, `admin-shutdown` `adminshutdown`, `shutdownadmin`, `shutdown-admin`

### Boostxp (admin only)
> It boost the xp for everyone until next restart (It changes the config.py file).
Usage: `boostxp <key> <value>`
Example of usage: `--boostxp addMessageMin 15`
Aliases: `xpboost`, `xp-boost`, `boost-xp`

### Savedb (admin only)
> It saves the database, for example saving users xps.
Usage: `savedb`
Example of usage: `--savedb`
Aliases: `save-db`, `save-database`, `db-save`, `dbsave`, `database-save`, `savedatabase`, `databasesave`

### Setxp (admin only)
> It sets the xp for a person in a specified guild.
Usage: `stexp <guild ID> <user ID> <xp>`
Example of usage: `--setxp 883621480007606282 699330746686373898 5000`