### PROGRAM
import discord
from discord.channel import VoiceChannel
from discord.ext import commands, tasks
import logging
from datetime import datetime
from random import randint
import sqlite3
from config import config
from time import time

# Init
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

# Functions
def registerDatabase(): # The fuction who will be executed when saving database
    logging.info("Started saving xp into database.")
    for guild in toadd:
        logging.debug("Started saving xp for guild " + str(guild))
        for user in toadd[guild]:
            if type(toadd[guild][user]) == int and type(guild) == int and type(user) == int:
                conn.execute("DELETE FROM content WHERE ID = " + str(user) + ";")
                conn.execute("INSERT INTO content(guild, id, xp) VALUES(" + str(guild) + "," + str(user) + "," + str(toadd[guild][user]) + ");")
                logging.debug("Saved " + str(toadd[guild][user]) + " xp for user " + str(user) + " in guild " + str(guild) + ".")
            else:
                sfile.write(str(user) + " or " + str(guild) + " or " + str(toadd[guild][user]) + " variables don't had good types (it musts be int) -- in saving database (line 31)")
        logging.debug("Ended save of xp for guild" + str(guild) + ".")
    conn.commit()
    logging.info("Ended save of xp into database.")

@tasks.loop(seconds = config["waitForRegiser"])
async def registerDatabaseTask():
    registerDatabase()

def shutdown(): # The function who will be executed when stopping the bot
    logging.info("Shutting down")
    registerDatabase()
    sfile.close()
    exit()

def addxp(guildid, userid, channelid, content=None):
    if channelid in config["ignoredChannels"]: # Check if channel is set to don't be recorded
        if content != None: logging.debug("Ignored xp promotion for user ID " + str(userid) + " containing \"" + str(content) + "\" because it was in an ignored channel, " + str(channelid) + " in guild " + str(guildid) + ".")
        else: logging.debug("Ignored xp promotion for user ID " + str(userid) + " because it was in an ignored channel, " + str(channelid)) + " in guild " + str(guildid) + "."
        return
    xp = randint(config["addMessageMin"], config["addMessageMax"])
    try:
        toadd[guildid][userid] += xp
    except KeyError:
        toadd[guildid][userid] = 0
    logging.debug(f"{userid} got {xp} xp.")

# Bot
@bot.event
async def on_ready():
    logging.info("Logged into Discord with " + str(bot.user.id))
    await bot.change_presence(status = discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name=config["registeringStatus"]))

    # Get guilds
    for guild in bot.guilds:
        toadd[guild.id] = {}
    for id in toadd:
        if type(id) == int:
            db = conn.execute("SELECT * FROM content WHERE guild=" + str(id) + ";")
            for thing in db:
                toadd[thing[0]][thing[1]] = thing[2]
        else:
            sfile.write("Guild ID " + str(id) + " didn't had a good type (it musts be int) -- in loading the guilds (line 61).")
    await bot.change_presence(status = discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=config["loadedStatus"]))
    logging.info("Registered database.")

    # Tasks
    registerDatabaseTask.start()
    voiceXpTask.start()

# XP
@bot.event 
async def on_message(message):
    await bot.process_commands(message)
    # Check timeout
    _returned = False
    try:
        if waitForMessages[message.author.id] + randint(config["messagesWaitForNextXpMin"], config["messagesWaitForNextXpMax"]) > time():
            _returned = True
            logging.debug("The user ID " + str(message.author.id) + " didn't got their xp because it was timeouted.")
            
    except KeyError:
        logging.debug("Inited or Timeouted message wait time for user ID " + str(message.author.id))
    if _returned == True: return # Return the function if the user didn't passed timeout

    waitForMessages[message.author.id] = time() # Reset timeout

    
    # Add xp
    addxp(message.guild.id, message.author.id, message.channel.id, message.content)

@tasks.loop(seconds = config["voiceWaitForNextXp"])
async def voiceXpTask():
    logging.debug("Started finding guilds for promoting voice XP")
    for guild in bot.guilds:
        logging.debug("Started promoting xp in guild " + str(guild.id))
        for channel in guild.channels:
            if type(channel) == discord.VoiceChannel:
                logging.debug("Starting registering XP for users in voice channel ID " + str(channel.id) + ".")
                for member in channel.members:
                    print("founded member")
                    addxp(guild.id, member.id, channel.id)
            else:
                logging.debug("Ignored channel ID " + str(channel.id) + " because it wasn't a voice channel.")

# Commands
@bot.command(aliases=["xp", "niveau", "niveaux", "level"])
async def levels(ctx, user : discord.User):
    
    xp = cursor.execute("SELECT xp FROM content WHERE id=" + str(user.id) + ";")
    for row in xp:
        print(str(row[0]))
    embed=discord.Embed()
    embed.add_field(name="XP of user " + str(user.name), value=str(row[0]), inline=False)
    await ctx.send(embed=embed)

# Admin commands
@bot.command(aliases = ["admin-stop", "adminstop", "stopadmin", "stop-admin", "shutdown", "admin-shutdown", "adminshutdown", "shutdownadmin", "shutdown-admin"])
async def stop(ctx):
    if ctx.author.id in config["ownerIds"]:
        await ctx.send(":warning: If you started the bot from an automatic restart script (maded by us), please save the database and stop it by terminating the process (use CTRL+C in the terminal window).")
        shutdown()

# Errors
@bot.event
async def on_command_error(ctx, error):
    await ctx.send(":x: Your command cannot be executed due to " + str(error) + "\nPlease re-try or contact a staff member.")
    logging.warning("\"" + str(error) + "\" after execution of \"" + str(ctx.message.content) + "\" by user ID " + str(ctx.message.author.id))

try:
    bot.run(config["token"])
    logging.critical("The bot has shut down. Saving database.")
    shutdown()
except discord.errors.LoginFailure as e:
    logging.critical("The provided token is invalid - " + str(e))
    print("The token your provided in the configuration is invalid, please replace it with a valid Discord bot token. If you don't know what that means, please contact us.")