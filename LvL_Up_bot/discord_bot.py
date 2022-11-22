import functools

import discord
from discord.ext import commands

from utils import update_member_levels, allowed_member, get_levelup_data, auto_levelup

from settings import server_id, roles_by_level, logs_channel_id, dev_id, mee6_id


class Bot(commands.Bot):
    logs_channel = None

    def auth(self, func):
        @functools.wraps(func)
        async def wrapper_decorator(*args, **kwargs):
            ctx = args[0]
            if ctx.guild is None or ctx.guild.id != server_id:
                if ctx.author.id == dev_id:
                    kwargs['DEBUG'] = True
                    return await func(*args, **kwargs)
                return
            if not allowed_member(ctx.author):
                command_name = func.__name__
                if len(args) > 1:
                    command_name += f' {args[1]}'
                await self.logs_channel.send(f'{ctx.author.mention} tried to use the command `{command_name}`.')
                return
            value = await func(*args, **kwargs)
            return value
        return wrapper_decorator


def discord_bot():
    description = '''TODO: finish this description haha.'''
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    bot = Bot(command_prefix='lv.', description=description, intents=intents)

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user} (ID: {bot.user.id})')
        print('------')
        guild = bot.get_guild(server_id)
        print(f'Guild: {guild.name} (ID: {guild.id})')
        print(f'Guild Members: {len(guild.members)}')
        for i, t in enumerate(roles_by_level):
            id, role_id = t
            roles_by_level[i] = (id, guild.get_role(role_id))
        print(f'Roles: {roles_by_level}')
        bot.logs_channel = guild.get_channel(logs_channel_id)

        # Auto-update
        send_function = bot.logs_channel.send
        updated_roles = await update_member_levels(bot.get_guild(server_id).get_member, send_function)
        if updated_roles:
            message = f'**{updated_roles}** level role{"s"*(updated_roles>1)} automatically updated while turning on.'
            print(message)
            await send_function(message)

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return
        # TODO: check also on config.py the other todos.
        if message.author.id == mee6_id:
            member_data = get_levelup_data(message)
            if member_data:
                get_member_function = bot.get_guild(server_id).get_member
                log_function = bot.logs_channel.send
                await auto_levelup(member_data, get_member_function, log_function)
        await bot.process_commands(message)

    @bot.command()
    @bot.auth
    async def ping(ctx, **kwargs):
        print('pong')
        await ctx.send('pong')

    @bot.command()
    @bot.auth
    async def update(ctx, *args, **kwargs):
        options = {'roles'}
        if len(args) != 1 or args[0] not in options:
            print('Usage: `lv.update roles`')
            await ctx.send('Usage: `lv.update roles`')
            return
        print('Checking levels...')
        send_function = bot.logs_channel.send
        if 'DEBUG' in kwargs and kwargs['DEBUG']:
            send_function = ctx.send
        await send_function('Checking levels...')
        updated_roles = await update_member_levels(bot.get_guild(server_id).get_member, send_function)
        if not updated_roles:
            message = 'No level roles to update'
        else:
            message = f'Done, **{updated_roles}** level role{"s"*(updated_roles>1)} updated.'
        print(message)
        await send_function(message)
    return bot
