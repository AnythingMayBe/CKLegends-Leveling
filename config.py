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
    "ignoredChannels": [929076256513863770, 929076221072003123], # Replace these values with all channel ids you want users to don't get xp in, for example command bots channels.

    # MESSAGES CONFIG
    "addMessageMin": 3, # Replace that value with the minimum amount of points a person will get per message.
    "addMessageMax": 5, # Replace that value with the maximum amount of points a person will get per message.
    "messagesWaitForNextXpMin": 25.0, # Replace that value with the minimum time you want to wait before someone can get more points per messages.
    "messagesWaitForNextXpMax": 40.0, # Replace that value with the maximum time you want to wait before someone can get more points per messages.
    

    # VOICE CONFIG
    "voiceXpRewardMin": 6, # Replace that value with the minimum amount of points a person will get by being in a voice channel.
    "voiceXpRewardMax": 8, # Replace that value with the maximum amount of points a person will get by being in a voice channel.
    "voiceWaitForNextXp": 60.0, # Replace that value with the minimum time you want to wait before someone can get more points for being in voice channel.
}
# REWARDS
rewards = {
    1000: 929295857105387550, # Replace the first value with the minmum amount of xp you want, and replace the second value with the role's id.
    2500: 929295874473996298, # Replace the first value with the minmum amount of xp you want, and replace the second value with the role's id.
    5000: 929295887736397864 # Replace the first value with the minmum amount of xp you want, and replace the second value with the role's id.
}