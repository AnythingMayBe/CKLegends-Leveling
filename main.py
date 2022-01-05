### PROGRAM
import discord
from discord.ext import commands, tasks
import logging
from datetime import datetime
from random import randint
import sqlite3
from config import config

# SQLite Init
toadd = {}
waitForMessages = {} 
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
    xp = randint(config["addMessageMin"], config["addMessageMax"])
    try:
        toadd[message.guild.id][message.author.id] += xp
    except KeyError:
        toadd[message.guild.id][message.author.id] = 0
    logging.debug(f"{message.author.id} got {xp} xp.")

try:
    bot.run(config["token"])
except discord.errors.LoginFailure as e:
    logging.critical("The provided token is invalid - " + str(e))
    print("The token your provided in the configuration is invalid, please replace it with a valid Discord bot token. If you don't know what that means, please contact us.")