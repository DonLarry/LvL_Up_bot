import os
from discord import Member

import requests

from config import server_id, min_level_role, roles_by_level, allowed_users, allowed_roles, owner_id


def _get_member_data(player):
    return (
        int(player['id']),
        player['level'],
    )


def _add_members(members, players):
    for player in players:
        member_data = _get_member_data(player)
        if member_data[1] < min_level_role:
            return False
        members.append(member_data)
    return True


def _get_member_levels():
    mee6_token = os.getenv('MEE6_TOKEN')
    url = f'https://mee6.xyz/api/plugins/levels/leaderboard/{server_id}'
    headers = {'authorization': mee6_token}
    members = []
    # _add_members(members, requests.get(url, headers=headers).json()['players'])
    page = 0
    while True:
        response = requests.get(url, headers=headers, params={'page': page})
        if response.status_code != 200:
            break
        players = response.json()['players']
        if not players:
            break
        if not _add_members(members, players):
            break
        page += 1
    return members


def _get_roles_by_level(level):
    """Returns previous, and actual roles for a given member level."""
    assert level >= min_level_role
    broke = False
    for i in range(len(roles_by_level)):
        if level < roles_by_level[i][0]:
            broke = True
            break
    if i == 1:
        return None, roles_by_level[0][1]
    if broke:
        return roles_by_level[i-2][1], roles_by_level[i-1][1]
    return roles_by_level[i-1][1], roles_by_level[i][1]


async def _update_member(member_data, get_member_function, log_function):
    member_id = member_data[0]
    if member_id == owner_id:
        return
    member = get_member_function(member_id)
    if member is None:
        return
    old_role, new_role = _get_roles_by_level(member_data[1])
    # print()
    # print(member.roles)
    if new_role not in member.roles:
        print(f'Adding role {new_role.name} to {member.mention}...')
        await log_function(f'Adding role {new_role.name} to {member.mention}...')
        await member.add_roles(new_role)
        if old_role is not None:
            print(f'Removing role {old_role.name} from {member.mention}...')
            await log_function(f'Removing role {old_role.name} from {member.mention}...')
            await member.remove_roles(old_role, reason='New level role (replacing old one)')


async def update_member_levels(get_member_function, log_function):
    member_levels = _get_member_levels()
    # print(f'Member levels: {member_levels}')
    for member_data in member_levels:
        # print(member_data)
        await _update_member(member_data, get_member_function, log_function)


def _allowed_role(member):
    for role in member.roles:
        if role.id in allowed_roles:
            return True
    return False


def allowed_member(member):
    return member.id in allowed_users or _allowed_role(member)


if __name__ == '__main__':
    import os
    from dotenv import load_dotenv
    load_dotenv()
    member_levels = _get_member_levels()
    print(f'Possible members: {len(member_levels)}')
    import code
    code.interact(local=locals())