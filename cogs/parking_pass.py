"""
A cog extension for the parking pass function of the bot app
"""

import logging
import logging.config
import datetime as dt

import pytz
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_components import (
    create_select,
    create_select_option,
    create_actionrow,
    wait_for_component
)
from src.utils.DatabaseHelper import DatabaseHelper

"""
For a list of inbuilt checks:
https://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html#checksordpy.readthedocs.io/en/rewrite/ext/commands/api.html#checks
You could also create your own custom checks. Check out:
https://github.com/Rapptz/discord.py/blob/master/discord/ext/commands/core.py#L689
For a list of events:
https://discordpy.readthedocs.io/en/rewrite/api.html#event-reference
https://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html#event-reference
"""

tz = pytz.timezone('America/New_York')


def pass_log(guild_id, msg):
    """
    Write pass actions to log for download
    """
    with open(f'src/logs/{guild_id}_pass_log.txt', 'a') as txt:
        t_s = dt.datetime.now(tz).strftime('%d-%b-%y %H:%M:%S')
        txt.write(f'{t_s} - {msg}\n')


class ParkingPassCog(commands.Cog, name='Parking Pass Manager'):
    """
    Parking pass manager commands
    """

    def __init__(self, bot):
        self.logger = logging.getLogger(__name__)
        self.bot = bot
        self.db_h = DatabaseHelper('parkingPass')
        self.db_path = None

    def pass_validate(self, pass_num):
        """
        Checks length of pass_num and verifies all digits
        :param pass_num: pass_id from discord cmd
        :return: True if valid, else False
        """
        return bool(str(pass_num).isdigit() and len(str(pass_num)) == 5)

    def pass_select(self, guild_id, op=None):
        """
        Checks db for passes issued/returned and returns in a list
        :param guild_id:String:I'd from guild executing command
        :param op:Int:0 returns passes returned, 1 returns passes issued
        :return:passes:list of pass numbers
        """
        pass_list = []
        passes = []
        # Database path
        self.db_path = f'src/db/{guild_id}.db'
        status = self.db_h.select_passes(self.db_h.connection(self.db_path))
        if status:
            i = 0
            while i < len(status):
                for k, v in status[i].items():
                    if k == 'out':
                        if op is None:
                            pass_list.append(status[i]['pass_id'])
                        # 0 is passes returned, 1 is passes issued
                        elif v == int(op):
                            pass_list.append(status[i]['pass_id'])
                i += 1
            for i in pass_list:
                passes.append(create_select_option(str(i), value=str(i)))
            return passes

    @cog_ext.cog_slash(name="check_out", description="Check Out Pass")
    async def pass_out(self, ctx: SlashContext):
        """
        /check_out - Check out pass
        """
        # Guild id
        guild_id = ctx.guild_id
        pass_select = create_select(
            # Options in drop down select menu
            # Pass 0 to check returned passes
            options=self.pass_select(guild_id, 0),
            placeholder="Choose your pass #",
            custom_id="select",
        )
        pass_row = create_actionrow(pass_select)
        msg = await ctx.send("Passes available to check out:", components=[pass_row], hidden=True)
        while True:
            try:
                pass_num_ctx = await wait_for_component(
                    self.bot, components=pass_select, timeout=60
                )
                pass_select = pass_num_ctx.selected_options
                pass_num = pass_select[0]
                t_s = dt.datetime.now(tz).strftime('%d-%b-%y %H:%M:%S')
                # User who sent message
                author = ctx.author.name
                user_name = ctx.author.mention
                self.db_path = f'src/db/{guild_id}.db'
                # Validate parking pass number
                if self.pass_validate(pass_num):
                    out = self.db_h.check_out_flag(self.db_h.connection(self.db_path), pass_num)
                    if out is False:
                        self.db_h.update_pass(self.db_h.connection(self.db_path), pass_num,
                                              author, t_s, 1)
                        pass_log(guild_id, f'OUT - {author} checked out {pass_num}')
                        self.logger.info('Pass %s has been checked out by %s', pass_num, author)
                        await pass_num_ctx.send(f'Pass {pass_num} has been checked out', hidden=True)
                        return await pass_num_ctx.guild.system_channel.send(f'Pass {pass_num} has been checked '
                                                                            f'out by {user_name}')
            except TimeoutError:
                pass_row["components"][0]["disabled"] = True
                await msg.edit(content="Timed Out", components=[pass_row])
                break

    @pass_out.error
    async def pass_out_error(self, ctx: SlashContext, error):
        """
        Error catcher for pass_out command
        :param self:
        :param ctx:
        :param error:
        """
        msg = f'check out error: {error}'
        await ctx.send(msg, hidden=True)

    @cog_ext.cog_slash(name="check_in", description="Check In Pass")
    async def pass_in(self, ctx: SlashContext):
        """
        /check_in - Check in pass
        """
        # Guild id
        guild_id = ctx.guild_id
        pass_select = create_select(
            # Options in drop down select menu
            # Pass 1 to check issued passes
            options=self.pass_select(guild_id, 1),
            placeholder="Choose your pass #",
            custom_id="select",
        )
        pass_row = create_actionrow(pass_select)
        msg = await ctx.send("Passes available to check in:", components=[pass_row], hidden=True)
        while True:
            try:
                pass_num_ctx = await wait_for_component(
                    self.bot, components=pass_select, timeout=60
                )
                pass_select = pass_num_ctx.selected_options
                pass_num = pass_select[0]
                # User who sent message
                author = ctx.author.name
                user_name = ctx.author.mention
                self.db_path = f'src/db/{guild_id}.db'
                # Validate parking pass number
                if self.pass_validate(pass_num):
                    out = self.db_h.check_out_flag(self.db_h.connection(self.db_path), pass_num)
                    if out is True:
                        self.db_h.update_pass(self.db_h.connection(self.db_path), pass_num, 'none',
                                              'none', 0)
                        pass_log(guild_id, f'IN - {author} checked in {pass_num}')
                        self.logger.info('Pass %s has been checked in by %s', pass_num, author)
                        await pass_num_ctx.send(f'Pass {pass_num} has been checked in', hidden=True)
                        return await pass_num_ctx.guild.system_channel.send(f'Pass {pass_num} has been checked in '
                                                                            f'by {user_name}')
            except TimeoutError:
                pass_row["components"][0]["disabled"] = True
                await msg.edit(content="Timed Out", components=[pass_row])
                break

    @pass_in.error
    async def pass_in_error(self, ctx: SlashContext, error):
        """
        Error catcher for pass_in command
        :param ctx:
        :param error:
        """
        msg = f'check in error: {error}'
        await ctx.send(msg, hidden=True)

    @cog_ext.cog_slash(name="add", description="Add Pass")
    @commands.guild_only()
    @commands.has_any_role("supervisors", "admin")
    async def pass_add(self, ctx: SlashContext, pass_num):
        """
        /add [pass#] - Add pass
        """
        # Guild ID of guild that invoked command
        guild_id = ctx.guild_id
        # User who sent message
        author = ctx.author.name
        self.db_h.setup(guild_id)
        self.db_path = f'src/db/{guild_id}.db'
        # Validate parking pass number
        if self.pass_validate(pass_num):
            out = self.db_h.check_out_flag(self.db_h.connection(self.db_path), pass_num)
            if out is None:
                add_pass = self.db_h.add_pass(self.db_h.connection(self.db_path), pass_num, 0)
                if add_pass is True:
                    pass_log(guild_id, f'ADD - {author} added {pass_num}')
                    self.logger.info('%s added to %s by %s', pass_num, self.db_path, author)
                    await ctx.send(f'{pass_num} has been added to your pool...', hidden=True)
                    return await ctx.guild.system_channel.send(f'{pass_num} has been added to your pool...')
                else:
                    return await ctx.send(f'{pass_num} could not be added. Contact the developer',
                                          hidden=True)
            else:
                return await ctx.send(f'{pass_num} is already registered...', hidden=True)
        else:
            return await ctx.send('Not a valid parking pass number. Please try again...',
                                  hidden=True)

    @pass_add.error
    async def pass_add_error(self, ctx: SlashContext, error):
        """
        Error catcher for pass_add command
        :param ctx:
        :param error:
        """
        msg = f'add pass error: {error}'
        await ctx.send(msg, hidden=True)

    @cog_ext.cog_slash(name="del", description="Delete Pass")
    @commands.guild_only()
    @commands.has_any_role("supervisors", "admin")
    async def pass_del(self, ctx: SlashContext):
        """
        /del - Delete pass
        """
        # Guild id
        guild_id = ctx.guild_id
        pass_select = create_select(
            # Options in drop down select menu
            # Pass 0 to check returned passes
            options=self.pass_select(guild_id),
            placeholder="Choose your pass #",
            custom_id="select",
        )
        pass_row = create_actionrow(pass_select)
        msg = await ctx.send("Passes available to delete:", components=[pass_row], hidden=True)
        while True:
            try:
                pass_num_ctx = await wait_for_component(
                    self.bot, components=pass_select, timeout=60
                )
                pass_select = pass_num_ctx.selected_options
                pass_num = pass_select[0]
                # User who sent message
                author = ctx.author.name
                user_name = ctx.author.mention
                self.db_path = f'src/db/{guild_id}.db'
                # Validate parking pass number
                if self.pass_validate(pass_num):
                    del_pass = self.db_h.del_pass(self.db_h.connection(self.db_path), pass_num)
                    print(del_pass)
                    if del_pass is True:
                        pass_log(guild_id, f'DEL - {author} deleted {pass_num}')
                        self.logger.info('Pass %s deleted from %s by %s', pass_num, self.db_path,
                                         author)
                        await pass_num_ctx.send(f'Pass {pass_num} has been deleted from your pool by {user_name}',
                                                hidden=True)
                        return await pass_num_ctx.guild.system_channel.send(f'Pass {pass_num} has been deleted '
                                                                            f'from your pool by {user_name}')
            except TimeoutError:
                pass_row["components"][0]["disabled"] = True
                await msg.edit(content="Timed Out", components=[pass_row])
                break

    @pass_del.error
    async def pass_del_error(self, ctx: SlashContext, error):
        """
        Error catcher for pass_del command
        :param ctx:
        :param error:
        """
        msg = f'del pass error: {error}'
        await ctx.send(msg, hidden=True)

    @cog_ext.cog_slash(name="report", description="Report")
    @commands.guild_only()
    @commands.has_any_role("supervisors", "admin")
    async def report(self, ctx: SlashContext, str_all=None):
        """
        /report [all] - [All] Out pass report
        """
        # Guild id from message
        guild_id = ctx.guild_id
        self.db_path = f'src/db/{guild_id}.db'
        pass_status = self.db_h.select_passes(self.db_h.connection(self.db_path))
        if pass_status:
            if str_all is None:
                pass_status[:] = [row for row in pass_status if row['out'] != 0]
            p = []
            i = 0
            while i < len(pass_status):
                for k, v in pass_status[i].items():
                    key = k.replace('_', ' ').capitalize()
                    if k == 'out':
                        if v == 0:
                            v = 'Returned'
                        else:
                            v = 'Issued'
                    p.append(f'{key}: {v}')
                p.append('')
                i += 1
            embed = discord.Embed(
                title="📑 Parking Pass Report",
                description="\n".join(p),
                color=0x5865F2,
            )
            embed.set_footer(text="Made with Python | https://github.com/tinfins/",
                             icon_url="https://i.imgur.com/5BFecvA.png")
            return await ctx.send(embed=embed, hidden=True)
        else:
            return await ctx.send('No parking passes are registered...', hidden=True)

    @report.error
    async def report_error(self, ctx: SlashContext, error):
        """
        Error catcher for report command
        :param ctx:
        :param error:
        """
        msg = f'report error: {error}'
        await ctx.send(msg, hidden=True)

    @cog_ext.cog_slash(name="get_file", description="Get File Report")
    @commands.guild_only()
    @commands.has_any_role("supervisors", "admin")
    async def get_file(self, ctx: SlashContext):
        """
        /get_file - Download file report
        """
        # Guild id from message
        guild_id = ctx.guild_id
        file = discord.File(f'src/logs/{guild_id}_pass_log.txt')
        return await ctx.send(file=file, content='Parking Pass Log', hidden=True)

    @report.error
    async def get_file_error(self, ctx: SlashContext, error):
        """
        Error catcher for report command
        :param ctx:
        :param error:
        """
        msg = f'file error: {error}'
        await ctx.send(msg, hidden=True)

    @cog_ext.cog_slash(name="help", description="Parking Pass Bot Help")
    async def help(self, ctx: SlashContext):
        """
        /help - Help file
        """
        embed = discord.Embed(
            title="⚠️ Parking Pass Bot Commands:",
            description="All Parking Pass Bot commands",
            color=0xED4245,
        )
        embed.add_field(name="/check_out", value="   - Select pass from drop-down to check out the pass")
        embed.add_field(name="/check_in", value="   - Select pass from drop-down to return the pass.")
        embed.add_field(name=" These commands are limited:", value="Supervisor role and above")
        embed.add_field(name="/add", value="   - Add passes to the pool. 5 digit pass number must be sent with command")
        embed.add_field(name="del", value="   - Select pass from drop-down to delete from pool")
        embed.add_field(name="/report",
                        value="   - Return list of issued passes. Optional value of 'all' returns status of all passes")
        embed.add_field(name="/get_file", value="   - Return bot history in text file")
        embed.set_footer(text="Made with Python | https://github.com/tinfins/",
                         icon_url="https://i.imgur.com/5BFecvA.png")
        return await ctx.send(embed=embed)


def setup(bot):
    """
    Adds cog to bot
    """
    bot.add_cog(ParkingPassCog(bot))
