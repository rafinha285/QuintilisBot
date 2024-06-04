import mongo_types
import asyncio
import mongodb_utils
async def makeClanResponse(clan:mongo_types.Clan):
    clan_name = clan['name']
    member_ids = clan['members']
    members = []
    points = clan['points']
    owner = (await mongodb_utils.get_player(clan['owner']))["name"]
    acronym = clan['prefix']
    enemies_ids = clan["enemies"]
    enemies = []
    allies_ids = clan["allies"]
    allies = []
    
    members_tasks = []
    enemies_tasks = []
    allies_tasks = []

    for member_id in member_ids:
        members_tasks.append(mongodb_utils.get_player(member_id))

    for enemy_id in enemies_ids:
        enemies_tasks.append(mongodb_utils.get_clan(enemy_id))

    for ally_id in allies_ids:
        allies_tasks.append(mongodb_utils.get_clan(ally_id))

    members = await asyncio.gather(*members_tasks)
    enemies = await asyncio.gather(*enemies_tasks)
    allies = await asyncio.gather(*allies_tasks)

    members_str = ", ".join(member["name"] for member in members)
    enemies_str = ", ".join(enemy["name"] for enemy in enemies)
    allies_str = ", ".join(ally["name"] for ally in allies)

    response = (f"CLAN: {clan_name}\n"
                f"\tMembros: {members_str}\n"
                f"\tHonras: {points}\n"
                f"\tDono: {owner}\n"
                f"\tSigla: {acronym}\n"
                f"\tInimigos: {enemies_str}\n"
                f"\tAliados: {allies_str}")
    return response