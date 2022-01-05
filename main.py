### PROGRAM
import discord
from discord.ext import commands, tasks
import logging
from datetime import datetime
from random import randint
import sqlite3
from config import config
from time import time

# SQLite Init
toadd = {}
waitForMessages = {} 
conn = sqlite3.connect("xp.db")
cursor = conn.cursor()

def registerDatabase():
    logging.info("Started saving xp into database.")
    for guild in toadd:
        logging.debug("Started saving xp for guild " + str(guild))
        for user in toadd[guild]:
            conn.execute("DELETE FROM content WHERE ID = " + str(user) + ";")
            conn.execute("INSERT INTO content(guild, id, xp) VALUES(" + str(guild) + "," + str(user) + "," + str(toadd[guild][user]) + ");")
            logging.debug("Saved " + str(toadd[guild][user]) + " xp for user " + str(user) + " in guild " + str(guild) + ".")
        logging.debug("Ended save of xp for guild" + str(guild) + ".")
    conn.commit()
    logging.info("Ended save of xp into database.")

@tasks.loop(seconds = config["waitForRegiser"])
async def registerDatabaseTask():
    registerDatabase()

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
    logging.info("Logged into Discord with " + str(bot.user.id))
    await bot.change_presence(status = discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name=config["registeringStatus"]))

    # Get guilds
    for guild in bot.guilds:
        toadd[guild.id] = {}
    for id in toadd:
        db = conn.execute("SELECT * FROM content WHERE guild=" + str(id) + ";")
        for thing in db:
            toadd[thing[0]][thing[1]] = thing[2]
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