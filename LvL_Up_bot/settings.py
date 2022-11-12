DEBUG = False
DISCORD_BOT_TOKEN_TEST = None

from local_settings import *

if DEBUG:
    DISCORD_BOT_TOKEN = DISCORD_BOT_TOKEN_TEST
