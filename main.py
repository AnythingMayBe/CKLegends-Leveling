### CONFIGURATION
config = {
    # GLOBAL CONFIG
    "token": "ODc4NTgwNDU2NzA5MjkyMDUz.YSDP0A.r9rVd2_M2Vyk1M7-NgzL1w7FPrI", # Replace that value with your Discord bot token, available on https://discord.com/developers/applications
    "prefix": "--", # Replace that value with the prefix of your bot, for example . or /
    "shards": 1, # Replace that with the value you want for shards (I recommend using one per 100 servers)
    "waitForRegiser": 300, # Replace that value with the time you want to wait before saving xp into database

    # MESSAGES CONFIG
    "addMessageMin": 3, # Replace that value with the minimum amount of points a person will get per message
    "addMessageMax": 5, # Replace that value with the maximum amount of points a person will get per message
    "messagesWaitForNextXp": 30.0, # Replace that value with the time you want to wait before someone can get more points per messages

    # VOICE CONFIG
    "voiceXpRewardMin": 6, # Replace that value with the minimum amount of points a person will get by being in a voice channel.
    "voiceXpRewardMax": 8, # Replace that value with the maximum amount of points a person will get by being in a voice channel.
    "voixeWaitForNextXp": 60.0 # Replace that value with the time you want to wait before someone can get more points for being in voice channel.
}

### PROGRAM
import discord
from discord.ext import commands, tasks
import logging
from datetime import datetime
import random
import sqlite3

# SQLite Init
toadd = {}
conn = sqlite3.connect("xp.db")
cursor = conn.cursor()

@tasks.loop(seconds = config["waitForRegiser"])
async def registerDatabase():
    logging.info("Started registering xp into database.")
    for guild in toadd:
        logging.debug("Started registering xp for guild " + str(guild))
        for user in toadd[guild]:
            conn.execute("DELETE FROM content WHERE ID = " + str(user) + ";")
            conn.execute("INSERT INTO content(guild, id, xp) VALUES(" + str(guild) + "," + str(user) + "," + str(toadd[guild][user]) + ");")
            logging.debug("Registered " + str(toadd[guild][user]) + " xp for user " + str(user) + " in guild " + str(guild) + ".")
        logging.debug("Ended registering xp for guild" + str(guild) + ".")
    conn.commit()
    logging.info("Ended registering xp into database.")

# Logging
logging.basicConfig(filename="logs/" + datetime.now().strftime("%h-%d-%y") + ".txt",
                        filemode='a',
                        format='[%(asctime)s,%(msecs)d] [%(name)s] [%(levelname)s] [%(message)s]',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG
)

# Bot
bot = commands.AutoShardedBot(command_prefix=config["prefix"], shard_count=config["shards"])

@bot.event
async def on_ready():
    logging.info("Logged into Discord.")
    # Get guilds
    for guild in bot.guilds:
        toadd[guild.id] = {}
    for id in toadd:
        db = conn.execute("SELECT * FROM content WHERE guild=" + str(id) + ";")
        for thing in db:
            toadd[thing[0]][thing[1]] = thing[2]
    logging.info("Registered database.")
    registerDatabase.start()


@bot.event 
async def on_message(message):
    xp = random.randint(config["addMessageMin"], config["addMessageMax"])
    try:
        toadd[message.guild.id][message.author.id] += xp
    except KeyError:
        toadd[message.guild.id][message.author.id] = 0
    logging.debug(f"{message.author.id} got {xp} xp.")

bot.run(config["token"])
