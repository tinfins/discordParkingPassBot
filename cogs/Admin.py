import logging.config
from discord.ext import commands
import discord

class Admin(commands.Cog, name='Parking Pass Manager'):
    """Admin-only commands that make the bot dynamic."""

    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)

    @commands.command(hidden=True)
    @commands.has_any_role("admin")
    async def load(self, *, module : str):
        '''
        Loads a module.
        '''
        try:
            self.bot.load_extension(module)
        except Exception as e:
            await self.bot.say('\N{PISTOL}')
            await self.bot.say('{}: {}'.format(type(e).__name__, e))
        else:
            self.logger.info(f'{str} loaded')
            await self.bot.say('\N{OK HAND SIGN}')

    @commands.command(hidden=True)
    @commands.has_any_role("admin")
    async def unload(self, *, module : str):
        '''
        Unloads a module.
        '''
        try:
            self.bot.unload_extension(module)
        except Exception as e:
            await self.bot.say('\N{PISTOL}')
            await self.bot.say('{}: {}'.format(type(e).__name__, e))
        else:
            self.logger.info(f'{str} unloaded')
            await self.bot.say('\N{OK HAND SIGN}')

    @commands.command(name='reload', hidden=True)
    @commands.has_any_role("admin")
    async def _reload(self, *, module : str):
        '''
        Reloads a module.
        '''
        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
        except Exception as e:
            await self.bot.say('\N{PISTOL}')
            await self.bot.say('{}: {}'.format(type(e).__name__, e))
        else:
            await self.bot.say('\N{OK HAND SIGN}')

def setup(bot):
    bot.add_cog(Admin(bot))
