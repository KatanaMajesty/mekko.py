# -*- coding: utf8 -*-
import discord
from discord.ext import commands
import json
import mojang
from mojang import MojangAPI
import requests
import datetime

class User(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(aliases=['dsuser', 'dsUser','discorduser','userinfo','member','memberinfo'])
    async def DUser(self, ctx, *, member:discord.Member = None):
        if member is None:
            await ctx.send('Укажи пользователя!')
            return
        else:
            status = member.status
            if str(status) == 'dnd':
                state = 'https://emoji.gg/assets/emoji/8874_DND_Oxzy.png'
            elif str(status) == 'online':
                state = 'https://emoji.gg/assets/emoji/9722_online_oxzy.png'
            elif str(status) == 'idle':
                state = 'https://emoji.gg/assets/emoji/3488_Idle_oxzy.png'
            elif str(status) == 'offline':
                state = 'https://emoji.gg/assets/emoji/1184_offline_oxzy.png'
            joined = member.joined_at.timestamp()
            guildtime = int((datetime.datetime.now().timestamp() - joined) / (60 * 60 * 24))
            members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
            pos = str(members.index(member)+1)
            roles = str(len(member.roles))
            if roles == 1:
                role = '**1** роль'
            else:
                role = f'**{roles}** роли/ей'

            embed_ds = discord.Embed(description=f'Ник **`{member.display_name}`**\nID **{member.id}**\nУ него {role}\n\nДата создания {member.created_at.strftime("**%Y.%m.%d** в **%H:%M**")}\nДата присоеденения {member.joined_at.strftime("**%Y.%m.%d** в **%H:%M**")}\nПрисоеденился **{pos}-ым**\nНа сервере уже **{guildtime}** дня', colour=discord.Colour.blurple())
            ava = member.avatar_url
            embed_ds.set_thumbnail(url=ava)
            embed_ds.set_author(name = f"Информация об участнике", icon_url = state)
            await ctx.send(embed=embed_ds)

def setup(client):
    client.add_cog(User(client))
