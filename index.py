import json;
import nextcord
from nextcord.ext import commands
from nextcord import Interaction


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


bot.run(TOKEN)