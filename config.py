import os

from dotenv import load_dotenv


load_dotenv()


DEBUG = True

server_id = int(os.getenv('SERVER_ID'))
min_level_role = 5
roles_by_level = [
    (5, int(os.getenv('LEVEL_ROLE_ID_1'))),
    (10, int(os.getenv('LEVEL_ROLE_ID_2'))),
    (15, int(os.getenv('LEVEL_ROLE_ID_3'))),
    (20, int(os.getenv('LEVEL_ROLE_ID_4'))),
    (25, int(os.getenv('LEVEL_ROLE_ID_5'))),
    (30, int(os.getenv('LEVEL_ROLE_ID_6'))),
    (35, int(os.getenv('LEVEL_ROLE_ID_7'))),
    (40, int(os.getenv('LEVEL_ROLE_ID_8'))),
    (50, int(os.getenv('LEVEL_ROLE_ID_9'))),
]
owner_id = int(os.getenv('OWNER_ID'))
allowed_users = {
    owner_id,
}
allowed_roles = {
    int(os.getenv('ALLOWED_ROLE_ID_1')),
}
logs_channel_id = int(os.getenv('LOGS_CHANNEL_ID'))
# TODO: add a function that returns a role, and a member if the message is a mee6 levelup message.
# TODO: do it for both servers (debug server, and main server).

if DEBUG:
    server_id = int(os.getenv('DEBUG_SERVER_ID'))
    min_level_role = 1
    roles_by_level = [
        (1, int(os.getenv('DEBUG_LEVEL_ROLE_ID_1'))),
        (3, int(os.getenv('DEBUG_LEVEL_ROLE_ID_2'))),
        (6, int(os.getenv('DEBUG_LEVEL_ROLE_ID_3'))),
    ]
    allowed_users = {
        -1, # No one
    }
    allowed_roles = {
        int(os.getenv('DEBUG_ALLOWED_ROLE_ID_1')),
    }
    logs_channel_id = int(os.getenv('DEBUG_LOGS_CHANNEL_ID'))
