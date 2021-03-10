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

    @commands.command(aliases=['muser', 'Muser','minecraftuser','player','playerinfo'])
    async def MUser(self, ctx, nick = None):
        try:
            if nick is None:
                await ctx.send('Укажи майнкрафт ник!')
                return
            uuid = MojangAPI.get_uuid(nick)

            model = f'https://crafatar.com/avatars/{uuid}?size=256&default=MHF_Steve&overlay'
            histor = MojangAPI.get_name_history(uuid)
            history = (int(len(MojangAPI.get_name_history(uuid))) - 1)
            profile = f'https://ru.namemc.com/profile/{nick}'

            url = f'https://minecraft-statistic.net/api/player/info/{nick}/'
            response = requests.get(url)
            pt = response.json()["data"]["total_time_play"]

            url2 = f'https://minecraft-statistic.net/api/player/info/{nick}/'
            response = requests.get(url)
            state = response.json()["data"]["online"]

            if state <= 0:
                status = '**оффлайн** :new_moon:'
            else:
                status = '**онлайн** :full_moon:'

            for data in histor:
                    if history > 0:
                        embed_mine = discord.Embed(title="Информация об игроке", description=f"Ник **{nick}**\nUUID **{uuid}**\nИзменял ник **{history}** раз\nCейчас {status}\nНаиграл **{pt}** часов на серверах\n[Профиль {nick}'a на NameMc]({profile})", colour=discord.Colour.blurple())
                        embed_mine.set_thumbnail(url=model)
                        embed_mine.set_footer(text='Данные взяты с "minecraft-statistic.net" и могут быть не точными')
                        await ctx.send(embed=embed_mine)
                        return
                    if history == 0:
                        embed_mine = discord.Embed(title="Информация об игроке",description=f"Ник **{nick}**\nUUID **{uuid}**\nИгрок не менял ник\nCейчас {status}\nНаиграл **{pt}** часов на серверах\n[Профиль {nick}'a на NameMc]({profile})",colour=discord.Colour.blurple())
                        embed_mine.set_thumbnail(url=model)
                        embed_mine.set_footer(text='Данные взяты с "minecraft-statistic.net" и могут быть не точными')
                        await ctx.send(embed=embed_mine)
                        return
        except:
            await ctx.send('Ошибка! Неверно указан ник или игрока нету в базе данных, из-за недавнего сбоя в базе данных "minecraft-statistic.net"')
    @commands.command(aliases=['skin', 'Skin'])
    async def MSkin(self, ctx, nick=None):
        if nick is None:
            await ctx.send('Укажи ник майнкрафт!')
            return
        try:
            url = f'https://api.mojang.com/users/profiles/minecraft/{nick}?'
            response = requests.get(url)
            name = response.json()['name']
            uuid = MojangAPI.get_uuid(nick)
            skin = f'https://crafatar.com/skins/{uuid}?size=64&default=MHF_Steve&overlay'
            model = f'https://crafatar.com/renders/body/{uuid}?size=512&default=MHF_Steve&overlay'
            embed_skin = discord.Embed(title=f'Скин игрока {nick}', description=f"[Cкачать скин]({skin})", colour=discord.Colour.blurple())
            embed_skin.set_image(url=model)
            await ctx.send(embed=embed_skin)
        except:
            await ctx.send('Ошибка! Ник указан неверно или не удалось получить скин игрока')


    @commands.command(aliases=['dsuser', 'dsUser','discorduser','userinfo','member','memberinfo'])
    async def DUser(self, ctx, member:discord.Member = None):
        if member is None:
            await ctx.send('Укажи участника!')
            return
        joined = member.joined_at.timestamp()
        guildtime = int((datetime.datetime.now().timestamp() - joined) / (60 * 60 * 24))

        embed_ds = discord.Embed(title="Информация об участнике",description=f'Ник **{member.display_name}**\nID **{member.id}**\nДата создания {member.created_at.strftime("**%Y.%m.%d** в **%H:%M**")}\nДата присоеденения {member.joined_at.strftime("**%Y.%m.%d** в **%H:%M**")}\nНа сервере уже **{guildtime}** дня', colour=discord.Colour.blurple())
        ava = member.avatar_url
        embed_ds.set_thumbnail(url=ava)
        await ctx.send(embed=embed_ds)

def setup(client):
    client.add_cog(User(client))