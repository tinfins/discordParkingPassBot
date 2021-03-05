import discord
from discord.ext import commands
from dotenv import load_dotenv
import pathlib
import os
from os import listdir
from os.path import isfile, join, dirname
from os import environ
import sys
import traceback
import datetime as dt
import pytz

#This is a multi file example showcasing many features of the command extension and the use of cogs.
#These are examples only and are not intended to be used as a fully functioning bot. Rather they should give you a basic
#understanding and platform for creating your own bot.
#These examples make use of Python 3.6.2 and the rewrite version on the lib.
#For examples on cogs for the async version:
#https://gist.github.com/leovoel/46cd89ed6a8f41fd09c5
#Rewrite Documentation:
#http://discordpy.readthedocs.io/en/rewrite/api.html
#Rewrite Commands Documentation:
#http://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html
#Familiarising yourself with the documentation will greatly help you in creating your bot and using cogs.


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    # Notice how you can use spaces in prefixes. Try to keep them simple though.
    prefixes = ['/','#','!']

    # Check to see if we are outside of a guild. e.g DM's etc.
    #if not message.guild:
    #    # Only allow / to be used in DMs
    #    return '/'

    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)


# Below cogs represents our folder our cogs are in. Following is the file name. So 'meme.py' in cogs, would be cogs.meme
# Think of it like a dot path import
# This is the directory all are located in.
cogs_dir = "cogs"

intents = discord.Intents(members=True,messages=True,guilds=True)

bot = commands.Bot(command_prefix=get_prefix, description='A parking pass manager. Prefix your commands with / or # or ! ',intents=intents)

# Here we load our extensions(cogs) that are located in the cogs directory. Any file in here attempts to load.
if __name__ == '__main__':
#@bot.event
#async def on_ready():
    for extension in [f.replace('.py', '') for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))]:
        try:
            bot.load_extension(cogs_dir + "." + extension)
            print(f'Loaded {extension} successfully')
        except (discord.ClientException, ModuleNotFoundError):
            print(f'Failed to load extension {extension}.')
            traceback.print_exc()

@bot.event
async def on_ready():
    """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready"""
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="/help, #help, and !help"))
    tz = pytz.timezone('America/New_York')
    ts = dt.datetime.now(tz).strftime('%d-%b-%m %H:%M:%S')
    print(f'\n{ts} EST')
    print('-'*15)
    print(f'Successfully logged in and booted...!')
    print(f'Logged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}')
    print('-'*15)

# Start the Server
#keep_alive.keep_alive()

#def run():
bot.run(TOKEN)