import functools

import discord
from discord.ext import commands

from utils import update_member_levels, allowed_member

from config import server_id, roles_by_level, logs_channel_id


class Bot(commands.Bot):
    logs_channel = None

    def auth(self, func):
        @functools.wraps(func)
        async def wrapper_decorator(*args, **kwargs):
            ctx = args[0]
            if ctx.guild is None or ctx.guild.id != server_id:
                if ctx.author.id == 668439228430155816:
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
        # TODO: after doing the function to update the levels by listening for mee6 levelup messages,
        #       do the following things:
        #       1. update member levels every time on_ready is executed
        #       2. delete the update command, so the bot automatically updates the levels

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return
        # TODO: check if the message is a mee6 levelup message, and if so, look if the member level role should be updated.
        # TODO: check also on config.py the other todos.
        # print(f'{message.author}: {message.content}')
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
            print('Usage: `lvl.update roles`')
            await ctx.send('Usage: `lvl.update roles`')
            return
        print('Updating levels...')
        send_function = bot.logs_channel.send
        if 'DEBUG' in kwargs and kwargs['DEBUG']:
            send_function = ctx.send
        await send_function('Updating levels...')
        await update_member_levels(bot.get_guild(server_id).get_member, send_function)
        print('Done!')
        await send_function('Done!')
    return bot
