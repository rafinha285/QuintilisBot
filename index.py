import json;
import nextcord
from nextcord.ext import commands
from nextcord import Interaction
import asyncio


import mongodb_utils
import mongo_types
import prometheus_utils
from handle import *

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
async def checkServer():
    if not await prometheus_utils.check_minecraft_status():
        channel = bot.get_channel(int(CHANNEL_ID))
        await channel.send("O servidor Minecraft está caído!")

@bot.slash_command(name="status",description="Checa o status")
async def checkStatus(ctx: Interaction):
    if await prometheus_utils.check_minecraft_status():
        await ctx.send("O servidor Minecraft está ligado.")
    else:
        await ctx.send("O servidor Minecraft está desligado.")

@bot.slash_command(name="clan_info", description="Obtém informações sobre um clã")
async def getClanCommand(interaction: nextcord.Interaction, clan_name: str):
    try:
        clan = await mongodb_utils.get_clan(clan_name)

        response = await makeClanResponse(clan)
        if interaction.response.is_done():
            await interaction.response.edit_message(content=response)
        else:
            await interaction.response.send_message(response)
    except ValueError as e:
        print(e)
        response = str(e)
        # print(interaction)
    

@bot.slash_command(name="top_clans",description="Mostra os melhores clãs")
async def getBestClansCommand(interaction:Interaction):
    try:
        clans = await mongodb_utils.get_all_clans()
        def sortAlg(e:mongo_types.Clan):
            return e["points"]
        clans.sort(key=sortAlg)

        response=""
    except ValueError as e:
        response = str(e)
    finally:
        if interaction.response.is_done():
            await interaction.response.edit_message(content=response)
        else:
            await interaction.response.send_message(response)

bot.run(TOKEN)