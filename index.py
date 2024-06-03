import json;
import nextcord
from nextcord.ext import commands
from nextcord import Interaction
import asyncio


import mongodb_utils
import prometheus_utils

with open("./config.json") as config_file:
    configs = json.load(config_file)
TOKEN = configs["token"]
CHANNEL_ID = configs["channel_id"]
PROMETHEUS_URL = configs["prometheus_url"]
MONGO_URI = configs["mongo_uri"]
MONGO_DATABASE = configs["mongo_database"]
PLAYER_COLLECTION = configs["player_collection"]
CLANS_COLLECTION = configs["clans_collection"]



intents = nextcord.Intents.default()
intents.messages = True

bot = commands.Bot(command_prefix="!",intents=intents)
# slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_ready():
    print("jao cu")

@bot.slash_command(name="ping", description="Responde com Pong!")
async def on_command(interaction:Interaction):
    await interaction.response.send_message("Pong!")

@bot.event
async def check_server():
    if not await prometheus_utils.check_minecraft_status():
        channel = bot.get_channel(int(CHANNEL_ID))
        await channel.send("O servidor Minecraft está caído!")

@bot.slash_command(name="status",description="Checa o status")
async def check_status(ctx: Interaction):
    if await prometheus_utils.check_minecraft_status():
        await ctx.send("O servidor Minecraft está ligado.")
    else:
        await ctx.send("O servidor Minecraft está desligado.")

@bot.slash_command(name="clan_info", description="Obtém informações sobre um clã")
async def get_clan_command(interaction: nextcord.Interaction, clan_name: str):
    try:
        clan = await mongodb_utils.get_clan(clan_name)

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
    except ValueError as e:
        response = str(e)
    if interaction.response.is_done():
        await interaction.response.edit_message(content=response)
    else:
        await interaction.response.send_message(response)

bot.run(TOKEN)