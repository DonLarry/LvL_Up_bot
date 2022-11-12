import os

from discord_bot import discord_bot

from settings import DISCORD_BOT_TOKEN


if __name__ == '__main__':
    bot = discord_bot()
    bot.run(DISCORD_BOT_TOKEN)
