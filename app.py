"""
This module loads the token, cogs, and runs the bot app
"""

import logging.config
import os
from os import listdir
from os.path import isfile, join
import traceback
import discord
from discord.ext import commands
from discord_slash import SlashCommand
from dotenv import load_dotenv, find_dotenv
from src.utils.DatabaseHelper import DatabaseHelper

# For examples on cogs for the async version:
# https://gist.github.com/leovoel/46cd89ed6a8f41fd09c5
# Rewrite Documentation:
# https://discordpy.readthedocs.io/en/rewrite/api.html
# Rewrite Commands Documentation:
# https://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html
# Familiarising yourself with the documentation will greatly help you in creating your bot and using cogs.

# Load Discord secret token from .env file
load_dotenv(find_dotenv())
TOKEN = os.getenv('PARKINGPASSBOT_TOKEN')

# Set up logging for application to write to
logging.config.fileConfig(fname='src/utils/config.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

# Cog directory. 'meme.py' in cogs directory is be cogs.meme
cogs_dir = "cogs"

bot = commands.Bot(command_prefix="!", description='A parking pass manager using slash commands', self_bot=True,
                   intents=discord.Intents.default())
slash = SlashCommand(bot, sync_commands=True)

# Load the extensions(cogs) that are located in the cogs directory. Any file in here attempts to load.
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
    """https://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_ready"""
    print('Successfully logged in and booted...!')
    print(f'Logged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}')
    logger.info('Successfully logged in and booted...!')
    logger.info('Logged in as: %s - %s\nVersion: %s', bot.user.name, bot.user.id, discord.__version__)


@bot.event
async def on_guild_join(guild):
    """https://discordpy.readthedocs.io/en/rewrite/api.html#discord.on_guild_join"""
    db_h = DatabaseHelper('parkingPass')
    db_h.setup(guild.id)
    print(f'Joined guild: {guild.id}')
    logger.info('Joined guild: %s', guild.id)


bot.run(TOKEN, bot=True, reconnect=True)
