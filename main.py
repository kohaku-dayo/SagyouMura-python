from asyncio.windows_events import NULL
import discord
from discord import app_commands
import os

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
intents.message_content = True

TOKEN = os.getenv("DISCORD_TOKEN")
guild_prod_id = os.getenv("guild_prod_id")
guild_test_id = os.getenv("guild_test_id")
custom_vc_category_prod_id = os.getenv("custom_vc_category_prod_id")
custom_vc_category_test_id = os.getenv("custom_vc_category_test_id")
guild_prod:discord.Guild = NULL
guild_test:discord.Guild = NULL
custom_vc_category_prod:discord.CategoryChannel = NULL
custom_vc_category_test:discord.CategoryChannel = NULL

@client.event
async def on_ready():
    print('ログインしました')
    addCommands()
    await tree.sync()
    guild_prod = client.get_guild(guild_prod)
    guild_test = client.get_guild(guild_test)
    custom_vc_category_prod = discord.utils.get(guild_prod, id=custom_vc_category_prod_id)
    custom_vc_category_test = discord.utils.get(guild_test, id=custom_vc_category_test_id)
    

def addCommands():
    tree.add_command(
        discord.app_commands.ContextMenu(
            name="VCを作成する",
            callback=on_create_vc_context,
            type=discord.AppCommandType.message,
            nsfw=False,
            auto_locale_strings=True
        )
    )
def isProd(guild_id: int): return guild_id == custom_vc_category_prod_id
def isTest(guild_id: int): return guild_id == custom_vc_category_test_id
def isInChannel(member: discord.Member): return member.voice.channel != None

async def on_create_vc_context(inter:discord.Interaction, message: discord.Message):
    if isProd(inter.guild.id):
        if isInChannel(inter.user):
            await inter.user.send(content="適当なVCに接続してから再度お試しください", mention_author=True)
            return
        await custom_vc_category_prod.create_voice_channel(f'{inter.user.global_name}の部屋')
    if isTest(inter.guild.id):
        if isInChannel(inter.user):
            await inter.user.send(content="適当なVCに接続してから再度お試しください", mention_author=True)
            return
        await custom_vc_category_test.create_voice_channel(f'{inter.user.global_name}の部屋')

@client.event
async def on_voice_state_update(member:discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    if isProd(member.guild.id):
        if before.channel == None and after.channel != None: on_prod_voice_state_join()
        if before.channel != None and after.channel == None: on_prod_voice_state_leave()
        if before.channel != None and after.channel != None: on_prod_voice_state_change()
    if isTest(member.guild.id):
        if before.channel == None and after.channel != None: on_test_voice_state_join()
        if before.channel != None and after.channel == None: on_test_voice_state_leave()
        if before.channel != None and after.channel != None: on_test_voice_state_change()

async def on_prod_voice_state_join():
    return
async def on_prod_voice_state_leave():
    return
async def on_prod_voice_state_change():
    return
async def on_test_voice_state_join():
    return
async def on_test_voice_state_leave():
    return
async def on_test_voice_state_change():
    return

@client.event
async def on_interaction(inter: discord.Interaction):
    return

client.run(TOKEN)