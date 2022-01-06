### PROGRAM
import discord
from discord.ext import commands, tasks
import logging
from datetime import datetime
from random import randint
import sqlite3
from config import config
from time import time
import re

# Init Init
bot = commands.AutoShardedBot(command_prefix=config["prefix"], shard_count=config["shards"]) # Bot object, used for all actions maded by the bot (not the program)
sfile = open("security/logs/" + datetime.now().strftime("%h-%d-%y"), 'a') # Security file log
toadd = {} # Temp variable (saved with SQLite) containing guilds and user xps
waitForMessages = {} # Temp variable containing users timeout before they can got xp
conn = sqlite3.connect("xp.db") # Temp variable containing the SQLite connection.
cursor = conn.cursor() # Temp variable containing the cursor of SQLite database.
logging.basicConfig(filename="logs/" + datetime.now().strftime("%h-%d-%y") + ".txt",
                        filemode='a',
                        format='[%(asctime)s,%(msecs)d] [%(name)s] [%(levelname)s] [%(message)s]',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG
) # The logging object (used for log everything logged, excepted security logs)

def registerDatabase():
    logging.info("Started saving xp into database.")
    for guild in toadd:
        logging.debug("Started saving xp for guild " + str(guild))
        for user in toadd[guild]:
            if re.search("/[\t\r\n]|(--[^\r\n]*)|(\/\*[\w\W]*?(?=\*)\*\/)/gi", str(user)) == None and re.search("/[\t\r\n]|(--[^\r\n]*)|(\/\*[\w\W]*?(?=\*)\*\/)/gi", str(guild)) == None and re.search("/[\t\r\n]|(--[^\r\n]*)|(\/\*[\w\W]*?(?=\*)\*\/)/gi", str(toadd[guild[user]])) == None:
                conn.execute("DELETE FROM content WHERE ID = " + str(user) + ";")
                conn.execute("INSERT INTO content(guild, id, xp) VALUES(" + str(guild) + "," + str(user) + "," + str(toadd[guild][user]) + ");")
                logging.debug("Saved " + str(toadd[guild][user]) + " xp for user " + str(user) + " in guild " + str(guild) + ".")
            else:
                sfile.write(str(user) + " or " + str(guild) + " or " + str(toadd[guild][user]) + " matched with our regex detection on database save (line 25)")
        logging.debug("Ended save of xp for guild" + str(guild) + ".")
    conn.commit()
    logging.info("Ended save of xp into database.")

@tasks.loop(seconds = config["waitForRegiser"])
async def registerDatabaseTask():
    registerDatabase()


# Bot
@bot.event
async def on_ready():
    logging.info("Logged into Discord with " + str(bot.user.id))
    await bot.change_presence(status = discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name=config["registeringStatus"]))

    # Get guilds
    for guild in bot.guilds:
        toadd[guild.id] = {}
    for id in toadd:
        if re.search("/[\t\r\n]|(--[^\r\n]*)|(\/\*[\w\W]*?(?=\*)\*\/)/gi", str(id)) == None:
            db = conn.execute("SELECT * FROM content WHERE guild=" + str(id) + ";")
            for thing in db:
                toadd[thing[0]][thing[1]] = thing[2]
        else:
            sfile.write("Guild ID " + str(id) + " matched with our regex detection -- in loading the guilds (line 55).")
    await bot.change_presence(status = discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=config["loadedStatus"]))
    logging.info("Registered database.")
    registerDatabaseTask.start()


@bot.event 
async def on_message(message):
    _returned = False
    try:
        if waitForMessages[message.author.id] + config["messagesWaitForNextXp"] > time():
            _returned = True
            logging.debug("The user ID " + str(message.author.id) + "didn't got their xp. (" + str(waitForMessages[message.author.id]) + " + " + str(config["messageWaitforNextXp"] + " < " + time()) + ")")
            
    except KeyError:
        logging.debug("Inited or Timeouted message wait time for user ID " + str(message.author.id))
    if _returned == True: return # Return the function if the user didn't passed timeout

    waitForMessages[message.author.id] = time() # Reset timeout

    # Add xp
    xp = randint(config["addMessageMin"], config["addMessageMax"])
    try:
        toadd[message.guild.id][message.author.id] += xp
    except KeyError:
        toadd[message.guild.id][message.author.id] = 0
    logging.debug(f"{message.author.id} got {xp} xp.")

try:
    bot.run(config["token"])
    logging.critical("The bot has shut down. Saving database.")
    registerDatabase()
except discord.errors.LoginFailure as e:
    logging.critical("The provided token is invalid - " + str(e))
    print("The token your provided in the configuration is invalid, please replace it with a valid Discord bot token. If you don't know what that means, please contact us.")