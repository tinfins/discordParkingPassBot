import discord
from discord.ext import commands
import logging.config
import datetime as dt
import pytz

"""A simple cog example with simple commands. Showcased here are some check decorators, and the use of events in cogs.
For a list of inbuilt checks:
http://dischttp://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html#checksordpy.readthedocs.io/en/rewrite/ext/commands/api.html#checks
You could also create your own custom checks. Check out:
https://github.com/Rapptz/discord.py/blob/master/discord/ext/commands/core.py#L689
For a list of events:
http://discordpy.readthedocs.io/en/rewrite/api.html#event-reference
http://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html#event-reference
"""

class ParkingPassCog(commands.Cog, name='Parking Pass'):
    '''
    Parking pass manager commands
    '''

    def __init__(self, bot):
        self.logger = logging.getLogger(__name__)
        self.bot = bot
        self.tz = pytz.timezone('America/New_York')

    @commands.command(name='pass', aliases = ['park'])
    async def pass_mngr(self, ctx, arg1, arg2):
        '''
        Manage parking passes.
        /pass [pass #] out - Check out parking pass
        /pass [pass #] in - Return parking pass
        '''
        ts = dt.datetime.now(self.tz).strftime('%d-%b-%y %H:%M:%S')
        user = ctx.message.author.mention
        if arg2 == 'out':
            await ctx.send(f'Parking pass {arg1} checked {arg2} by {user} at {ts}')
            self.logger.info(f"{ctx.author} has checked {arg2} pass {arg1}'")
        elif arg2 == 'in':
            await ctx.send(f'Parking pass {arg1} checked {arg2} by {user} at {ts}')
            self.logger.info(f"{ctx.author} has checked {arg2} pass {arg1}'")
        
    
    @commands.command(name='passadmin')
    @commands.guild_only()
    @commands.has_any_role("supervisors", "admin")
    async def navadmin(self, ctx, arg1, arg2):
        '''
        /passadmin [pass #] add - Add pass to database
        /passadmin [pass#] del - Delete pass from database
        '''
        ts = dt.datetime.now(self.tz).strftime('%d-%b-%y %H:%M:%S')
        user = ctx.message.author.mention
        if arg2 == 'add':
            await ctx.send(f'Parking pass {arg1} checked {arg2} by {user} at {ts}')
            self.logger.info(f"{ctx.author} has checked {arg2} pass {arg1}'")
        elif arg2 == 'del':
            await ctx.send(f'Parking pass {arg1} checked {arg2} by {user} at {ts}')
            self.logger.info(f"{ctx.author} has checked {arg2} pass {arg1}'")
        else:
            await ctx.send(f'{ctx} {arg2} not found')


# The setup function below is neccesarry. Remember we give bot.add_cog() the name of the class in this case SimpleCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(ParkingPassCog(bot))