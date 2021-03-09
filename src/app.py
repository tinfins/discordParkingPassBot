import logging.config
import os
from os import listdir
from os.path import isfile, join
import traceback
import discord
from discord.ext import commands
from dotenv import load_dotenv
from utils.DatabaseHelper import DatabaseHelper

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
TOKEN = os.getenv('PARKINGPASSBOT_TOKEN')

logging.config.fileConfig(fname='src/utils/config.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

def get_prefix(bot, message):
    """A callable Prefix for our bot. This could be edited to allow per server prefixes."""

    # Prefix is pass or park. Should eliminate any overlap with any other bots
    prefixes = ['/pass', '#pass', '/park', '#park']

    # If we are in a guild, we allow for the user to mention us or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)


# Below cogs represents our folder our cogs are in. Following is the file name. So 'meme.py' in cogs, would be cogs.meme
# Think of it like a dot path import
# This is the directory all are located in.
cogs_dir = "cogs"

intents = discord.Intents(members=True,messages=True,guilds=True)

bot = commands.Bot(command_prefix=get_prefix, description='A parking pass manager. Prefix your commands with /pass or #pass',intents=intents)

# Here we load our extensions(cogs) that are located in the cogs directory. Any file in here attempts to load.
if __name__ == '__main__':
    for extension in [f.replace('.py', '') for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))]:
        try:
            bot.load_extension(cogs_dir + "." + extension)
            print(f'Loaded {extension} successfully')
            logger.info('Loaded %s successfully', extension)
        except (discord.ClientException, ModuleNotFoundError):
            print(f'Failed to load extension: {extension}')
            print(discord.ClientException)
            print(ModuleNotFoundError)
            logger.error('Failed to load extension: %s', extension)
            traceback.print_exc()

@bot.event
async def on_ready():
    """http://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready"""
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="/pass help, #pass help"))
    print('Successfully logged in and booted...!')
    print(f'Logged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}')
    logger.info('Successfully logged in and booted...!')
    logger.info('Logged in as: %s - %s\nVersion: %s', bot.user.name, bot.user.id, discord.__version__)

@bot.event
async def on_guild_join(guild):
    dbH = DatabaseHelper('parkingPass')
    dbH.setup(guild.id)
    print(f'Joined guild: {guild.id}')
    logger.info('Joined guild: %s', guild.id)

@bot.event
async def on_guild_remove(guild):
    os.remove(f'src/db/{guild.id}.db')
    print(f'Removed from guild: {guild.id}')
    logger.info('Removed from guild: %s', guild.id)

bot.run(TOKEN)
