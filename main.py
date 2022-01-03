### CONFIGURATION
config = {
    # GLOBAL CONFIG
    "token": "DISCORD_BOT_TOKEN", # Replace that value with your Discord bot token, available on https://discord.com/developers/applications
    "prefix": "--", # Replace that value with the prefix of your bot, for example . or /
    "onRunMessages": True, # Replace that with "False" if you don't want to get a message when it will run, with "True" if you want to.
    "shards": 1, # Replace that with the value you want for shards (I recommend using one per 100 servers)

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
from discord.ext import commands

bot = commands.AutoShardedBot(command_prefix=config["prefix"], shard_count=config["shards"])

bot.run(config["token"])