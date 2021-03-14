import logging.config
from discord.ext import commands
import discord

class Admin(commands.Cog, name='Admin'):
    """Admin-only commands that make the bot dynamic."""

    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)

    @commands.command(name='load')
    @commands.has_any_role("admin")
    async def load(self, ctx, *, module : str):
        '''
        Loads a module.
        '''
        try:
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.send('\N{PISTOL}')
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            self.logger.info(f'{str} loaded')
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command(name='unload')
    @commands.has_any_role("admin")
    async def unload(self, ctx, *, module : str):
        '''
        Unloads a module.
        '''
        try:
            self.bot.unload_extension(module)
        except Exception as e:
            await ctx.send('\N{PISTOL}')
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            self.logger.info(f'{str} unloaded')
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command(name='reload')
    @commands.has_any_role("admin")
    async def _reload(self, ctx, *, module : str):
        '''
        Reloads a module.
        '''
        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.send('\N{PISTOL}')
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('\N{OK HAND SIGN}')

def setup(bot):
    bot.add_cog(Admin(bot))
