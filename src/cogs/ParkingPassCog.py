import logging.config
import datetime as dt
import pytz
import discord
from discord.ext import commands
from utils.DatabaseHelper import DatabaseHelper


"""A simple cog example with simple commands. Showcased here are some check decorators, and the use of events in cogs.
For a list of inbuilt checks:
http://dischttp://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html#checksordpy.readthedocs.io/en/rewrite/ext/commands/api.html#checks
You could also create your own custom checks. Check out:
https://github.com/Rapptz/discord.py/blob/master/discord/ext/commands/core.py#L689
For a list of events:
http://discordpy.readthedocs.io/en/rewrite/api.html#event-reference
http://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html#event-reference
"""


class ParkingPassCog(commands.Cog, name='Parking Pass Manager'):
    '''
    Parking pass manager commands
    '''
    def __init__(self, bot):
        self.logger = logging.getLogger(__name__)
        self.bot = bot
        self.tz = pytz.timezone('America/New_York')
        # Sqlite handler initialization
        self.dbH = DatabaseHelper('parkingPass')
        self.db_path = None

    def pass_validate(self, pass_num):
        '''
        Checks length of pass_num and verifies all digits
        :param pass_num: pass_id from discord cmd
        :return: True if valid, else False
        '''
        return bool(str(pass_num).isdigit() and len(str(pass_num)) == 5)

    @commands.command(name='out')
    async def pass_out(self, ctx, pass_num):
        '''
        /pass out [pass #] - Check out parking pass
        '''
        ts = dt.datetime.now(self.tz).strftime('%d-%b-%y %H:%M:%S')
        # User who sent message
        author = ctx.author
        user_name = author.name
        # Guild id from message
        guild_id = ctx.message.guild.id
        self.db_path = f'src/db/{guild_id}.db'
        # Validate parking pass number
        if self.pass_validate(pass_num):
            out = self.dbH.check_out_flag(self.dbH.connection(self.db_path), pass_num)
            if out is False:
                self.dbH.update_pass(self.dbH.connection(self.db_path), pass_num, user_name, ts, 1)
                print(f'Pass {pass_num} has been checked out by {user_name}')
                self.logger.info('Pass %s has been checked out by %s', pass_num, user_name)
                return await ctx.send(f'Pass {pass_num} has been checked out by {user_name}')
            elif out is True:
                return await ctx.send(f'{pass_num} is already checked out. Mark this pass as returned or check out a different parking pass...')
            elif out is None:
                return await ctx.send(f'{pass_num} does not exist...')
        else:
            return await ctx.send('Not a valid parking pass number. Please try again...')
    
    @pass_out.error
    async def pass_out_error(self, ctx, error):
        msg = f'check out error: {error}'
        await ctx.send(msg)
    
    @commands.command(name='in')
    async def pass_in(self, ctx, pass_num):
        '''
        /pass in [pass #] - Check in parking pass
        '''
        # User who sent message
        author = ctx.author
        user_name = author.name
        # Guild id from message
        guild_id = ctx.message.guild.id
        self.db_path = f'src/db/{guild_id}.db'
        # Validate parking pass number
        if self.pass_validate(pass_num):
            out = self.dbH.check_out_flag(self.dbH.connection(self.db_path), pass_num)
            if out is True:
                self.dbH.update_pass(self.dbH.connection(self.db_path), pass_num, 'none', 'none', 0)
                print(f'Pass {pass_num} has been checked in by {user_name}')
                self.logger.info('Pass %s has been checked in by %s', pass_num, user_name)
                return await ctx.send(f'Pass {pass_num} has been checked in by {user_name}')
            elif out is False:
                return await ctx.send(f'{pass_num} has already been turned in...')
            elif out is None:
                return await ctx.send(f'{pass_num} not found...')
        else:
            return await ctx.send('Not a valid parking pass number. Please try again...')
    
    @pass_in.error
    async def pass_in_error(self, ctx, error):
        msg = f'check in error: {error}'
        await ctx.send(msg)
        
    @commands.command(name='add')
    @commands.guild_only()
    @commands.has_any_role("supervisors", "admin")
    async def pass_add(self, ctx, pass_num):
        '''
        /pass add [pass #] - Add pass to database
        '''
        # User who sent message
        author = ctx.author
        user_name = author.name
        # Guild id from message
        guild_id = ctx.message.guild.id
        self.db_path = f'src/db/{guild_id}.db'
        # Validate parking pass number
        if self.pass_validate(pass_num):
            out = self.dbH.check_out_flag(self.dbH.connection(self.db_path), pass_num)
            if out is None:
                add_pass = self.dbH.add_pass(self.dbH.connection(self.db_path), pass_num, 0)
                if add_pass is True:
                    print(f'{pass_num} added to {self.db_path} by {user_name}')
                    self.logger.info('%s added to %s by %s', pass_num, self.db_path, user_name)
                    return await ctx.send(f'{pass_num} has been added to your pool...')
                else:
                    return await ctx.send(f'{pass_num} could not be added. Contact the developer')
            else:
                return await ctx.send(f'{pass_num} is already registered...')
        else:
            return await ctx.send('Not a valid parking pass number. Please try again...')
    
    @pass_add.error
    async def pass_add_error(self, ctx, error):
        msg = f'add pass error: {error}'
        await ctx.send(msg)
    
    @commands.command(name='del')
    @commands.guild_only()
    @commands.has_any_role("supervisors", "admin")
    async def pass_del(self, ctx, pass_num):
        '''
        /pass del [pass #] - Delete pass to database
        '''
        # User who sent message
        author = ctx.author
        user_name = author.name
        # Guild id from message
        guild_id = ctx.message.guild.id
        self.db_path = f'src/db/{guild_id}.db'
        # Validate parking pass number
        if self.pass_validate(pass_num):
            del_pass = self.dbH.del_pass(self.dbH.connection(self.db_path), pass_num)
            if del_pass:
                print(f'{pass_num} deleted from {self.db_path} by {user_name}')
                self.logger.info('%s deleted from %s by %s', pass_num, self.db_path, user_name)
                return await ctx.send(f'{pass_num} has been deleted from your pool...')
            else:
                return await ctx.send(f'{pass_num} could not be deleted. Contact the developer')
        else:
            return await ctx.send('Not a valid parking pass number. Please try again...')
    
    @pass_del.error
    async def pass_del_error(self, ctx, error):
        msg = f'del pass error: {error}'
        await ctx.send(msg)
    
    @commands.command(name='status')
    @commands.guild_only()
    @commands.has_any_role("supervisors", "admin")
    async def status(self, ctx, pass_num):
        '''
        /pass status [pass #] - Check status of pass
        '''
        # User who sent message
        author = ctx.author
        user_name = author.name
        # Guild id from message
        guild_id = ctx.message.guild.id
        self.db_path = f'src/db/{guild_id}.db'
        # Validate parking pass number
        if self.pass_validate(pass_num):
            status = self.dbH.check_pass(self.dbH.connection(self.db_path), pass_num)
            if status is None:
                return await ctx.send(f'{pass_num} does not exist')
            else:
                p = []
                for k, v in status[0].items():
                    key = k.replace('_', ' ').capitalize()
                    if k == 'out':
                        if v == 0:
                            v = 'Returned'
                        else:
                            v = 'Issued'
                    p.append(f'{key}: {v}')
                return await ctx.send("'\n'.join(p)")
        else:
            return await ctx.send('Not a valid parking pass number. Please try again...')
    
    @status.error
    async def status_error(self, ctx, error):
        msg = f'add pass error: {error}'
        await ctx.send(msg)
    
    @commands.command(name='report')
    @commands.guild_only()
    @commands.has_any_role("supervisors", "admin")
    async def report(self, ctx):
        '''
        /pass report - Show status of passes
        '''
        # User who sent message
        author = ctx.author
        user_name = author.name
        # Guild id from message
        guild_id = ctx.message.guild.id
        self.db_path = f'src/db/{guild_id}.db'
        status = self.dbH.select_passes(self.dbH.connection(self.db_path))
        if status is None:
            return await ctx.send(f'{self.db_path} does not exist')
        else:
            p = []
            i = 0
            while i < len(status):
                for k, v in status[i].items():
                    key = k.replace('_', ' ').capitalize()
                    if k == 'out':
                        if v == 0:
                            v = 'Returned'
                        else:
                            v = 'Issued'
                    p.append(f'{key}: {v}')
                p.append('')
                i += 1
            return await ctx.send('\n'.join(p))

    @report.error
    async def report_error(self, ctx, error):
        msg = f'report error: {error}'
        await ctx.send(msg)


# The setup function below is necessary. Remember we give bot.add_cog() the name of the class in this case SimpleCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(ParkingPassCog(bot))
