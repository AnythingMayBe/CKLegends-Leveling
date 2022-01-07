### CONFIGURATION
config = {
    # GLOBAL CONFIG
    "token": "ODc4NTgwNDU2NzA5MjkyMDUz.YSDP0A.VJuj7TFVXWeoNKi8Tp7uGv75IIg", # Replace that value with your Discord bot token, available on https://discord.com/developers/applications.
    "prefix": "--", # Replace that value with the prefix of your bot, for example . or /.
    "shards": 1, # Replace that with the value you want for shards (I recommend using one per 100 servers).
    "waitForRegiser": 300, # Replace that value with the time you want to wait before saving xp into database.
    "registeringStatus": "Registering database", # Replace that value with the status you want to have for your bot when loading database (at start).
    "loadedStatus": "Making you levels up.", # Replace that value with the status you want to have for you bot when it's loaded.
    "ownerIds": [854616353499906049, 699330746686373898], # Replace these values with the values you want for bot owners (they can execute all administrator commands)

    # MESSAGES CONFIG
    "addMessageMin": 3, # Replace that value with the minimum amount of points a person will get per message.
    "addMessageMax": 5, # Replace that value with the maximum amount of points a person will get per message.
    "messagesWaitForNextXp": 30.0, # Replace that value with the time you want to wait before someone can get more points per messages.

    # VOICE CONFIG
    "voiceXpRewardMin": 6, # Replace that value with the minimum amount of points a person will get by being in a voice channel.
    "voiceXpRewardMax": 8, # Replace that value with the maximum amount of points a person will get by being in a voice channel.
    "voixeWaitForNextXp": 60.0 # Replace that value with the time you want to wait before someone can get more points for being in voice channel.
}