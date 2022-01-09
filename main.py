### PROGRAM
import discord
from discord.channel import VoiceChannel
from discord.ext import commands, tasks
import logging
from datetime import datetime
from random import randint
import sqlite3
from config import config, rewards, store
from time import time
from asyncio import sleep

# Init
temp = {} # Temp variable used for lots of things
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
                sfile.write("[" + datetime() + "] " + str(user) + " or " + str(guild) + " or " + str(toadd[guild][user]) + " variables don't had good types (it musts be int) -- in saving database (line 33)")
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

def addxp(type, guild, user, channelid, content=None):
    if channelid in config["ignoredChannels"]: # Check if channel is set to don't be recorded
        if content != None: logging.debug("Ignored xp promotion for user ID " + str(user.id) + " containing \"" + str(content) + "\" because it was in an ignored channel, " + str(channelid) + " in guild " + str(guild.id) + ".")
        else: logging.debug("Ignored xp promotion for user ID " + str(user.id) + " because it was in an ignored channel, " + str(channelid)) + " in guild " + str(guild.id) + "."
        return
    if type == "chat": xp = randint(config["addMessageMin"], config["addMessageMax"])
    elif type == "voice": xp = randint(config["voiceXpRewardMin"], config["voiceXpRewardMax"])
    try:
        toadd[guild.id][user.id] += xp
    except KeyError:
        toadd[guild.id][user.id] = 0
    logging.debug(f"{user.id} got {xp} xp in guild " + str(guild.id) + ".")

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
            sfile.write("[" + datetime() + "] " + "Guild ID " + str(id) + " didn't had a good type (it musts be int) -- in loading the guilds (line 75).")
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
    addxp("chat", message.guild, message.author, message.channel.id, message.content)
    
    # Role Reward
    for reward in rewards:
        role = discord.utils.get(message.guild.roles, id=rewards[reward])
        if toadd[message.guild.id][message.author.id] > reward and role not in message.author.roles:
            await message.author.add_roles(role)
            msg = await message.channel.send(config["rewardMessage"])
            await sleep(config["rewardMessageDel"])
            await msg.delete()
            c = discord.utils.get(message.guild.channels, id=config["rewardChannelsAnnouncement"])
            await c.send(":clap: " + message.author.name + " got the role `" + str(role.name) + "` for their activity. Thanks!")

@tasks.loop(seconds = config["voiceWaitForNextXp"])
async def voiceXpTask():
    logging.debug("Started finding guilds for promoting voice XP")
    for guild in bot.guilds:
        logging.debug("Started promoting xp in guild " + str(guild.id))
        for channel in guild.channels:
            if type(channel) == discord.VoiceChannel:
                logging.debug("Starting registering XP for users in voice channel ID " + str(channel.id) + ".")
                for member in channel.members:
                    addxp("voice", guild, member, channel.id)
            else:
                logging.debug("Ignored channel ID " + str(channel.id) + " because it wasn't a voice channel.")

# Commands
@bot.command(aliases=["xp", "niveau", "niveaux", "level"])
async def levels(ctx, user : discord.User):
    if type(user.id) != int:
        sfile.write("[" + datetime() + "] " + "User ID " + str(user.id) + " is not an int.")
        await ctx.send(":x: The provided user is invalid.")
        return
    xp = cursor.execute("SELECT xp FROM content WHERE id=" + str(user.id) + ";")
    embed=discord.Embed()
    for row in xp:
        try:
            embed.add_field(name="XP of user " + str(user.name), value=str(row[0]), inline=False)
        except UnboundLocalError:
            embed.add_field(name="XP of user " + str(user.name), value="0", inline=False)
    await ctx.send(embed=embed)

@bot.command(aliases=["purchase", "buy", "store"])
async def shop(ctx, product : int =None):
    if product == None:
        r = ""
        for element in store:
            r += f"**{element}XP** {store[element]}\n"
        await ctx.send(":shopping_bags: Here is a list of everything you can get from our store:\n" + r)
        return
    temp[f"{ctx.author.name}-shop"] = 0
    for element in store:
        temp[f"{ctx.author.name}-shop"] += 1
        if temp[f"{ctx.author.name}-shop"] == int(product):
            try:
                toadd[ctx.guild.id][ctx.author.id] -= element
            except KeyError:
                toadd[ctx.guild.id][ctx.author.id] = -element
            await ctx.send("You successfully buyed **" + store[element] + "**\nAn administrator will contact you shortly.")
            c = discord.utils.get(ctx.guild.channels, id=config["rewardChannelsAnnouncement"])
            await c.send(f"{ctx.author.mention} purchased product ID **{product}**, name **{store[element]}** for **{element}** XP.")


# Admin commands
@bot.command(aliases = ["admin-stop", "adminstop", "stopadmin", "stop-admin", "shutdown", "admin-shutdown", "adminshutdown", "shutdownadmin", "shutdown-admin"])
async def stop(ctx):
    if ctx.author.id in config["ownerIds"]:
        await ctx.send(":warning: If you started the bot from an automatic restart script (maded by us), please save the database and stop it by terminating the process (use CTRL+C in the terminal window).")
        shutdown()

@bot.command(aliases=["xpboost", "xp-boost", "boost-xp"])
async def boostxp(ctx, key, value : int):
    if ctx.author.id in config["ownerIds"]:
        if key == "addMessageMin" or key == "addMessageMax" or key == "voiceXpRewardMin" or key == "voiceXpRewardMax":
            logging.info("Boost XP edited due to request of " + str(ctx.author.id) + ", " + str(key) + " was " + str(config[key]) + " and are now " + str(value))
            config[key] = value
            await ctx.send("Boost XP has successfully started. This will reset at next restart.")
        else:
            await ctx.send("Please specify the same key as in your config.")

@bot.command(aliases=["save-db", "save-database", "db-save", "dbsave", "database-save", "savedatabase", "databasesave"])
async def savedb(ctx):
    if ctx.author.id in config["ownerIds"]:
        msg = await ctx.send(":hourglass: Starting saving the database.")
        registerDatabase()
        await msg.edit(content=":white_check_mark: Saved database.")

@bot.command()
async def setxp(ctx, guild : int, user : int, xp : int):
    if ctx.author.id in config["ownerIds"]:
        toadd[guild][user] = xp
        await ctx.send(":white_check_mark: Successfully changed " + str(user) + " xp to " + str(xp))

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