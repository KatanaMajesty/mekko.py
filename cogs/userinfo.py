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
    async def MUser(self, ctx, *, nick = None):
        try:
            try:
                if nick is None:
                    await ctx.send('Укажи майнкрафт ник!')
                    return
                uuid = MojangAPI.get_uuid(nick)

                model = f'https://crafatar.com/avatars/{uuid}?size=256&default=MHF_Steve&overlay'
                history = (int(len(MojangAPI.get_name_history(uuid))) - 1)
                profile = f'https://ru.namemc.com/profile/{nick}'

                url = f'https://minecraft-statistic.net/api/player/info/{nick}/'
                response = requests.get(url)
                state = response.json()["data"]["online"]

                if state == 0:
                    status = 'https://emoji.gg/assets/emoji/1184_offline_oxzy.png'
                else:
                    status = 'https://emoji.gg/assets/emoji/9722_online_oxzy.png'

                if history > 0:
                    embed_mine = discord.Embed(description=f"Ник **`{nick}`**\nUUID **{uuid}**\nИзменял ник **{history}** раз\n[Профиль на NameMc]({profile})", colour=discord.Colour.blurple())
                    embed_mine.set_thumbnail(url=model)
                    embed_mine.set_author(icon_url=status, name='Информация об игроке')
                    embed_mine.set_footer(text='Данные взяты с "minecraft-statistic.net"\nПри указании ника убедитесь в соблюдении регистра!')
                    await ctx.send(embed=embed_mine)
                    return
                if history == 0:
                    embed_mine = discord.Embed(description=f"Ник **`{nick}`**\nUUID **{uuid}**\nИгрок не менял ник\n[Профиль на NameMc]({profile})",colour=discord.Colour.blurple())
                    embed_mine.set_thumbnail(url=model)
                    embed_mine.set_author(icon_url=status, name = 'Информация об игроке')
                    embed_mine.set_footer(text='Данные взяты с "minecraft-statistic.net"\nПри указании ника убедитесь в соблюдении регистра!')
                    await ctx.send(embed=embed_mine)
                    return
            except:
                    if nick is None:
                        await ctx.send('Укажи майнкрафт ник!')
                        return
                    uuid = MojangAPI.get_uuid(nick)

                    model = f'https://crafatar.com/avatars/{uuid}?size=256&default=MHF_Steve&overlay'
                    history = (int(len(MojangAPI.get_name_history(uuid))) - 1)
                    profile = f'https://ru.namemc.com/profile/{nick}'


                    if history > 0:
                        embed_mine = discord.Embed(description=f"Ник **`{nick}`**\nUUID **{uuid}**\nИзменял ник **{history}** раз\n[Профиль на NameMc]({profile})", colour=discord.Colour.blurple())
                        embed_mine.set_thumbnail(url=model)
                        embed_mine.set_author(icon_url='https://emoji.gg/assets/emoji/1666_Question.png', name='Информация об игроке')
                        embed_mine.set_footer(text='Игрока нет на "minecraft-statistic.net"\nПри указании ника убедитесь в соблюдении регистра!')
                        await ctx.send(embed=embed_mine)
                        return
                    if history == 0:
                        embed_mine = discord.Embed(description=f"Ник **`{nick}`**\nUUID **{uuid}**\nИгрок не менял ник\n[Профиль на NameMc]({profile})",colour=discord.Colour.blurple())
                        embed_mine.set_thumbnail(url=model)
                        embed_mine.set_author(icon_url='https://emoji.gg/assets/emoji/1666_Question.png', name='Информация об игроке')
                        embed_mine.set_footer(text='Игрока нет на "minecraft-statistic.net"\nПри указании ника убедитесь в соблюдении регистра!')
                        await ctx.send(embed=embed_mine)
                        return
        except:
            await ctx.send('Ошибка! Ник игрока указан неверно')


    @commands.command(aliases=['skin', 'Skin'])
    async def MSkin(self, ctx, *, nick=None):
        if nick is None:
            await ctx.send('Укажи ник майнкрафт!')
            return
        try:
            url = f'https://api.mojang.com/users/profiles/minecraft/{nick}?'
            head = '/give @s player_head{SkullOwner:' + f"\"{nick}\"" + '}'
            response = requests.get(url)
            name = response.json()['name']
            uuid = MojangAPI.get_uuid(nick)
            skin = f'https://crafatar.com/skins/{uuid}?size=64&default=MHF_Steve&overlay'
            model = f'https://crafatar.com/renders/body/{uuid}?size=512&default=MHF_Steve&overlay'
            embed = discord.Embed(description=f"**[Скин игрока {name}]({skin})**", colour=discord.Colour.blurple())
            embed.set_footer(text = f'Получить голову:\n{head}')
            embed.set_image(url=model)
            await ctx.send(embed=embed)
        except:
            await ctx.send('Ошибка! Ник указан неверно или не удалось получить скин игрока')

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