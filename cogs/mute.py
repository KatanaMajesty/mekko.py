import discord
from discord.ext import commands
from pymongo import MongoClient
from datetime import datetime, timedelta
import json
import asyncio

with open('config.json', 'r', encoding="utf-8") as file:
	config = json.load(file)

class User(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cluster = MongoClient("mongodb+srv://Bloodycat:PN1gkXf8H6Yf5X1P@chimekko-cluster.imrbn.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        self.mute = self.cluster.Chimekko_db.mute

    @commands.command(aliases=['m'])
    async def mute(self, ctx, member: discord.Member = None, time = None, *, reason = None):
        prefix = config["settings"]["prefix"]
        channel = self.client.get_channel(config['settings']['server_console'])
        channelmod = self.client.get_channel(config['settings']['log_moderator'])
        date = datetime.now().strftime("**%Y.%m.%d** в **%H.%M**")
        role = discord.utils.find(lambda r: r.id == config["settings"]["id_role_moderator"], ctx.guild.roles)
        author = ctx.author
        guild = ctx.guild

        bot = self.client.get_user(config["settings"]["id"])

        if member == bot:
            return
            
        if role in author.roles:
            if member is None:
                mute_in_bd = 0
                bd = self.mute.find({}, {"data": 1})
                for info in bd:
                    try:
                        x = info["data"]
                        mute_in_bd += 1
                    except:
                        continue

                embed = discord.Embed(description = f'**Мут пользователя\n\nУчастников в муте: `{mute_in_bd}`\nПосмотреть участника:\n`{prefix}mutes (участник)`\n\nПример команды:\n`{prefix}mute (участник) (время) (причина)`**', color = 0x2f3136)
                embed.set_thumbnail(url = self.client.user.avatar_url)
                await ctx.send(embed = embed)

                return

            mutebd = {"_id": member.id}
            mute_in_bd = self.mute.find_one({"_id": member.id})

            if self.mute.count_documents({"_id": member.id}) == 0:
                self.mute.insert_one(mutebd) 


            if time is None:
                embed = discord.Embed(description = f'**Ошибка ввода команды!\n`{prefix}mute (участник) (время) (причина)`\n\nПример:\n`{prefix}mute @member#1234 10m/20h/30d причина`**', color = 0x2f3136)
                await ctx.send(embed = embed)
                    
                return

            else:
                try:
                    for info in mute_in_bd:
                        if info == 'reason':
                            continue
                        if info == 'data':
                            embed = discord.Embed(description = f'**Этот участник уже в муте!**', color = 0x2f3136)
                            await ctx.send(embed = embed)

                            return
                except:
                    embed = discord.Embed(description = f'**В базе данных произошла ошибка, повторите запрос.**', color = 0x2f3136)
                    await ctx.send(embed = embed)

                    return
                    

                    
            if time[-1] == "s" or time[-1] == "S":
                sec = int(time[:-1])
            elif time[-1] == "m" or time[-1] == "M":
                sec = int(time[:-1])*60
            elif time[-1] == "h" or time[-1] == "H":
                sec = int(time[:-1])*60*60
            elif time[-1] == "d" or time[-1] == "D":
                sec = int(time[:-1])*60*60*24
            else:
                embed = discord.Embed(description = f'**Ошибка ввода команды!\n`{prefix}mute (участник) (время) (причина)`\n\nПример:\n`{prefix}mute @member#1234 10m/20h/30d причина`**', color = 0x2f3136)
                await ctx.send(embed = embed)

                return

            now = datetime.now()
            seco = timedelta(seconds=sec)
            x = now + seco
            data = str(x)[2:]
            date = x.strftime("%Y.%m.%d в %H:%M")

            for role in guild.roles:
                if role.id == config['mute']['role']:
                    await member.add_roles(role)
                    self.mute.update({"_id": member.id}, {"$set": {'data': data}})
                    self.mute.update({"_id": member.id}, {"$set": {'reason': reason}})

                    await channel.send(f'mute {member.display_name} {time} {reason}')

                    ava_moderator = author.avatar_url
                    ava_member = member.avatar_url
                    embed1 = discord.Embed(title='Логирование',description=f'{member.mention} успешно замучен на игровом сервере\nПричина: **{reason}**\nДлительность: **{time}** \n Дата мута {date}', colour=discord.Colour.red())
                    embed1.set_thumbnail(url=ava_member)
                    embed1.set_footer(text=f"Модератор: {author.display_name}", icon_url=ava_moderator)
                    await channelmod.send(embed=embed1)

                    embed = discord.Embed(description = f'**Мут выдан успешно!\n\n{member.mention} был замучен на `{seco}`\nМут будет снята: `{date}`\n\nПричина: `{reason}`**', color = 0x2f3136)
                    await ctx.send(embed = embed)
        else:
            embed = discord.Embed(description=f'**у вас нет прав!**')
            await ctx.send(embed=embed)

    @commands.command(aliases=['ms'])
    async def mutes(self, ctx, member: discord.Member = None):
        author = ctx.author

        if member is None:
            try:
                mute_in_bd = self.mute.find_one({"_id": author.id})

                date = mute_in_bd['data']
                reas = mute_in_bd['reason']

                date = datetime.strptime(date, '%y-%m-%d %H:%M:%S.%f').strftime("%Y.%m.%d в %H:%M")
            
                embed = discord.Embed(description = f"**Мут пользователя\n\nЗамучен: {author.mention}\nПричина: `{reas}`\nСрок заканчивается: `{date}`**", color = 0x2f3136)
                embed.set_thumbnail(url = author.avatar_url)
                await ctx.send(embed = embed)

                return
            except:
                embed = discord.Embed(description = f"**{author.mention} не в муте**", color = 0x2f3136)
                await ctx.send(embed = embed)

        else:
            try:
                mute_in_bd = self.mute.find_one({"_id": member.id})

                date = mute_in_bd['data']
                reas = mute_in_bd['reason']

                date = datetime.strptime(date, '%y-%m-%d %H:%M:%S.%f').strftime("%Y.%m.%d в %H:%M")
            
                embed = discord.Embed(description = f"**Мут пользователя\n\nЗамучен: {member.mention}\nПричина: `{reas}`\nСрок заканчивается: `{date}`**", color = 0x2f3136)
                embed.set_thumbnail(url = member.avatar_url)
                await ctx.send(embed = embed)

                return

            except:
                embed = discord.Embed(description = f"**{member.mention} не в муте**", color = 0x2f3136)
                await ctx.send(embed = embed)
    @commands.Cog.listener()
    async def on_message(self, message):
        content = message.content
        if '<@!227117061011144704>' in content or '<@!385425624082284544>' in content:
            await message.add_reaction("💖")

    @commands.command(aliases=['unm'])
    async def unmute(self, ctx, member: discord.Member = None):
        channel = self.client.get_channel(config['settings']['server_console'])
        channelmod = self.client.get_channel(config['settings']['log_moderator'])
        date = datetime.now().strftime("**%Y.%m.%d** в **%H.%M**")
        author = ctx.author
        ava_moderator = author.avatar_url
        ava_member = member.avatar_url

        if member is None:
            embed = discord.Embed(description = f"**Пользователь не указан!**", color = 0x2f3136)
            await ctx.send(embed = embed)
            
            return
        mute_in_bd = self.mute.find_one({"_id": member.id})

        for info in mute_in_bd:
            if info == '_id':
                continue
            if info == 'reason':
                continue
            if info == 'data':
                self.mute.update({"_id": member.id}, {"$unset": {'data': 1 }}) 
                self.mute.update({"_id": member.id}, {"$pull": {'data': 1}})

                embed1 = discord.Embed(title='Логирование', description=f'{member.mention} мут успешно снят на игровом сервере\n Дата снятия мута {date}',colour=discord.Colour.red())
                embed1.set_thumbnail(url=ava_member)
                embed1.set_footer(text=f"Модератор: {author.display_name}", icon_url=ava_moderator)
                await channelmod.send(embed=embed1)

                embed2 = discord.Embed(title='Снятие мута',description=f'{member.mention}, мут снят на игровом сервере',colour=discord.Colour.red())
                embed2.set_footer(text=f"Модератор: {author.display_name}", icon_url=ava_moderator)
                await member.send(embed=embed2)

                embed3 = discord.Embed(title='Мут', description=f'{member.mention} мут успешно снят на игровом сервере', colour=discord.Colour.red())
                embed3.set_footer(text=f"Модератор: {author.display_name}", icon_url=ava_moderator)
                await ctx.send(embed=embed3)

                await channel.send(f'unmute {member.display_name}')

                return

        embed = discord.Embed(description = f"**{member.mention} не в муте**", color = 0x2f3136)
        await ctx.send(embed = embed)        

    @commands.Cog.listener()
    async def on_ready(self):
        guild = discord.utils.get(self.client.guilds, name=config["settings"]["name_server"])
        for meber in guild.members:
            mutebd = {"_id": meber.id}
            if self.mute.count_documents({"_id": meber.id}) == 0:
                    self.mute.insert_one(mutebd) 

        while True:
            await asyncio.sleep(1)
            bd = self.mute.find({}, {"data": 1})
            for info in bd:
                now = datetime.now()
                try:
                    for role in guild.roles:
                        if role.id == config['mute']['role']:
                            member = discord.utils.get(guild.members, id=int(info['_id'])) 
                            date = datetime.strptime(info["data"], '%y-%m-%d %H:%M:%S.%f')
                            
                            if date < now or role not in member.roles:
                                date = datetime.now().strftime("**%Y.%m.%d** в **%H.%M**")
                                channel = self.client.get_channel(config['settings']['server_console'])
                                channelmod = self.client.get_channel(config['settings']['log_moderator'])
                                ava_member = member.avatar_url 
                                
                                await member.remove_roles(role)
                                await channel.send(f'unmute {member.display_name}')

                                self.mute.update({"_id": member.id}, {"$unset": {'data': 1 }}) 
                                self.mute.update({"_id": member.id}, {"$pull": {'data': 1}})

                                embed = discord.Embed(description=f"{member.mention}, с Вас сняли мут!\nПросим больше не нарушать правила сервера💖", colour=discord.Colour.light_gray())
                                await member.send(embed = embed)

                                embed1 = discord.Embed(title='Логирование', description=f'{member.mention} мут успешно снят на игровом сервере\n Дата снятия мута {date}',colour=discord.Colour.red())
                                embed1.set_thumbnail(url=ava_member)
                                await channelmod.send(embed=embed1)

                except:
                    continue

def setup(client):
    client.add_cog(User(client))