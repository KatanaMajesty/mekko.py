import discord
from discord.ext import commands
import json
import datetime
import asyncio
from pymongo import MongoClient

with open('config.json', 'r', encoding="utf-8") as file:
	config = json.load(file)

class User(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cluster = MongoClient("mongodb+srv://Bloodycat:PN1gkXf8H6Yf5X1P@chimekko-cluster.imrbn.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        self.application = self.cluster.Chimekko_db.application

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        print('1')
        prefix = config["settings"]["prefix"]
        message_id = payload.message_id
        guild = discord.utils.find(lambda g: g.id == payload.guild_id, self.client.guilds)
        author = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
        bot = self.client.get_user(config["settings"]["id"])
        application = self.application.find_one({"_id": author.id})
        application_all = self.application.find_one({"message": message_id})

        emoji = discord.utils.get(guild.emojis, name='wumpus_cozy')
        emoji2 = discord.utils.get(guild.emojis, name='m2_cateee')
        emoji3 = discord.utils.get(guild.emojis, name='wumpus_cookie')

        application_in_bd = {"_id": author.id, "number": 0}

        if self.application.count_documents({"_id": author.id}) == 0:
            self.application.insert_one(application_in_bd)   

        if author.id == bot.id:
            return
        if message_id == config["application"]["start_message"]: 
            if payload.emoji.id == 774769459265011712:
                try:
                    if application["number"] == 0:
                        self.application.update({"_id": author.id}, {"$set": {"number": 1}})

                        embed = discord.Embed(title= f"{emoji}  Привет!", description = f" Для подачи заявки ответь на следующие вопросы. Отвечай на вопросы максимально честно, **без нумерации** и **иных символов** в начале!\n Напиши: **{prefix}стоп** - для отмены заполнения заявки.", colour = discord.Colour.blurple())
                        await author.send(embed = embed)

                        embed = discord.Embed(description = config["application"]["question_1"], colour = discord.Colour.blurple())
                        await author.send(embed = embed)

                    elif application["number"] > 0:
                        print('6')
                        embed = discord.Embed(title = f"{emoji2} Ты не можешь подать заявку, так как не закончил предыдущую.", description = f"Напиши команду **{prefix}стоп** чтобы начать заного!", colour = discord.Colour.blurple())
                        await author.send(embed = embed)

                    else:
                        embed = discord.Embed(title = f"{emoji3} Ты уже отправил заявку!", description =  "Нам понадобится немного времени, чтобы рассмотреть её, прояви своё терпение.", colour = discord.Colour.red())
                        await author.send(embed = embed)
                except:
                    return
                    
            else:
                return

        else:
            try:
                channel = self.client.get_channel(config["application"]["id_channel"])
                message = await channel.fetch_message(application_all["message"])
                member = application_all["_id"]

                if payload.emoji.name == "✅":
                    question_1 = config["application"]["question_1"]
                    question_2 = config["application"]["question_2"]
                    question_3 = config["application"]["question_3"]
                    question_4 = config["application"]["question_4"]
                    question_5 = config["application"]["question_5"]
                    question_6 = config["application"]["question_6"]

                    app_question_1 = application_all["question_1"]
                    app_question_2 = application_all["question_2"]
                    app_question_3 = application_all["question_3"]
                    app_question_4 = application_all["question_4"]
                    app_question_5 = application_all["question_5"]
                    app_question_6 = application_all["question_6"]

                    user = self.client.get_user(int(member))
                    time = datetime.datetime.now().strftime("%Y.%m.%d в %H.%M")
                    uav1 = author.avatar_url
                    uav = user.avatar_url
                    emoji4 = discord.utils.get(guild.emojis, name='1upvote')

                    embed = discord.Embed(title = "**Заявка на Chimekko!**", description = f"**От:** {user.mention} (`Создан {user.created_at.strftime('%Y.%m.%d в %H:%M')}`)\n**{question_1}**\n`{app_question_1}`\n**{question_2}**\n`{app_question_2}`\n**{question_3}**\n`{app_question_3}`\n**{question_4}**\n`{app_question_4}`\n**{question_5}**\n`{app_question_5}`\n**{question_6}**\n`{app_question_6}`\n**Статус:** Утвердил - {author.mention}", colour = discord.Colour.green())
                    embed.set_footer(text = f"Дата: {time}", icon_url= uav1)
                    embed.set_thumbnail(url=uav)
                    await message.edit(embed = embed)
                    await message.remove_reaction("✅", bot)
                    await message.remove_reaction("⛔", bot)
                    await message.remove_reaction("✅", author)

                    channel_accept = self.client.get_channel(config["settings"]["server_console"])
                    await channel_accept.send(f"whitelist add {app_question_1}")
                    await channel_accept.send(f"kick -s {app_question_1} Ты принят на сервер, заверши регистрацию")
                    await channel_accept.send(f"discord link {app_question_1} {user.id}")
                    
                    embed = discord.Embed(title=f"{emoji4} Привет, {app_question_2}!", description= f"Я рад сообщить, что ты принят на наш проект Chimekko! IP-Адрес сервера - **join.chimekko.ru**. Твой Discord был привязан к нику, указанному в заявке. Если ты в режиме гостя, то проверь правильность написания ника и обратись к модерации проекта!\n Приятной игры :smiling_face_with_3_hearts: ", colour = discord.Colour.green())
                    await user.send(embed = embed)

                    self.application.remove({"_id": user.id})

                if payload.emoji.name == "⛔":
                        question_1 = config["application"]["question_1"]
                        question_2 = config["application"]["question_2"]
                        question_3 = config["application"]["question_3"]
                        question_4 = config["application"]["question_4"]
                        question_5 = config["application"]["question_5"]
                        question_6 = config["application"]["question_6"]

                        app_question_1 = application_all["question_1"]
                        app_question_2 = application_all["question_2"]
                        app_question_3 = application_all["question_3"]
                        app_question_4 = application_all["question_4"]
                        app_question_5 = application_all["question_5"]
                        app_question_6 = application_all["question_6"]

                        user = self.client.get_user(int(member))
                        time = datetime.datetime.now().strftime("%Y.%m.%d в %H.%M")
                        uav1 = author.avatar_url
                        uav = user.avatar_url
                        emoji5 = discord.utils.get(guild.emojis, name='1downvote')

                        embed = discord.Embed(title = "**Заявка на Chimekko!**", description = f"**От:** {user.mention} (`Создан {user.created_at.strftime('%Y.%m.%d в %H:%M')}`)\n**{question_1}**\n`{app_question_1}`\n**{question_2}**\n`{app_question_2}`\n**{question_3}**\n`{app_question_3}`\n**{question_4}**\n`{app_question_4}`\n**{question_5}**\n`{app_question_5}`\n**{question_6}**\n`{app_question_6}`\n**Статус:** Отклонил - {author.mention}", colour = discord.Colour.red())
                        embed.set_footer(text = f"Дата: {time}", icon_url= uav1)
                        embed.set_thumbnail(url=uav)
                        await message.edit(embed = embed)
                        await message.remove_reaction("✅", bot)
                        await message.remove_reaction("⛔", bot)
                        await message.remove_reaction("⛔", author)

                        self.application.update({"_id": user.id}, {"$set": {"number": 0}})

                        embed = discord.Embed(title=f"{emoji5} Привет, {app_question_2}!", description= "Твоя заявка была рассмотрена. К сожалению, она отклонена, так как модерация сервера не посчитала её качественной или твоих умений в строительстве недостаточно для игры на проекте. Заявку можно подать повторно при наличии желания. Если у тебя есть какие-либо вопросы - обратись к модерации проекта.", colour = discord.Colour.red())
                        await user.send(embed = embed)
            except:
                return
                
    @commands.command(aliases=['стоп'])
    async def application_stop(self, ctx):
        channel = ctx.message.channel
        author = ctx.message.author
        application = self.application.find_one({"_id": author.id})
        if application["number"] > 0:
            try:
                channels = ctx.message.guild.text_channels 
                if channel in channels:
                    return
            except:
                self.application.update({"_id": author.id}, {"$set": {"number": 0}})

                embed = discord.Embed(title = 'Заявка отменена!', colour = discord.Colour.red())
                await author.send(embed = embed)

        else:
            return

    @commands.Cog.listener()
    async def on_message(self, message):
        author = message.author
        content = message.content
        channel = message.channel
        uav = author.avatar_url
        await asyncio.sleep(0.1)
        application = self.application.find_one({"_id": author.id})
        bot = self.client.get_user(config["settings"]["id"])

        if author.id == bot.id:
            return
        if channel.id == 731078569136226375:
	    await message.delete(message)
        try:
            channels = message.guild.text_channels 
            if channel in channels:
                return
        except:
            if author.id == config["settings"]["id"]:
                return

            if application["number"] == 1:
                self.application.update({"_id": author.id}, {"$set": {"number": 2}})
                self.application.update({"_id": author.id}, {"$set": {"question_1": content}})

                embed = discord.Embed(description = config["application"]["question_2"], colour = discord.Colour.blurple())
                await author.send(embed = embed)

            elif application["number"] == 2:
                self.application.update({"_id": author.id}, {"$set": {"number": 3}})
                self.application.update({"_id": author.id}, {"$set": {"question_2": content}})

                embed = discord.Embed(description = config["application"]["question_3"], colour = discord.Colour.blurple())
                await author.send(embed = embed)

            elif application["number"] == 3:
                self.application.update({"_id": author.id}, {"$set": {"number": 4}})
                self.application.update({"_id": author.id}, {"$set": {"question_3": content}})

                embed = discord.Embed(description = config["application"]["question_4"], colour = discord.Colour.blurple())
                await author.send(embed = embed)

            elif application["number"] == 4:
                self.application.update({"_id": author.id}, {"$set": {"number": 5}})
                self.application.update({"_id": author.id}, {"$set": {"question_4": content}})

                embed = discord.Embed(description = config["application"]["question_5"], colour = discord.Colour.blurple())
                await author.send(embed = embed)

            elif application["number"] == 5:
                self.application.update({"_id": author.id}, {"$set": {"number": 6}})
                self.application.update({"_id": author.id}, {"$set": {"question_5": content}})

                embed = discord.Embed(description = config["application"]["question_6"], colour = discord.Colour.blurple())
                await author.send(embed = embed)

            elif application["number"] == 6:
                self.application.update({"_id": author.id}, {"$set": {"number": -1}})
                self.application.update({"_id": author.id}, {"$set": {"question_6": content}})
                
                question_1 = config["application"]["question_1"]
                question_2 = config["application"]["question_2"]
                question_3 = config["application"]["question_3"]
                question_4 = config["application"]["question_4"]
                question_5 = config["application"]["question_5"]
                question_6 = config["application"]["question_6"]

                app_question_1 = application["question_1"]
                app_question_2 = application["question_2"]
                app_question_3 = application["question_3"]
                app_question_4 = application["question_4"]
                app_question_5 = application["question_5"]
                app_question_6 = content
                
                time = datetime.datetime.now().strftime("%Y.%m.%d в %H.%M")
                channel_app = self.client.get_channel(config["application"]["id_channel"])

                embed = discord.Embed(title = "**Заявка на Chimekko!**", description = f"**От:** {author.mention} (`Создан {author.created_at.strftime('%Y.%m.%d в %H:%M')}`)\n**{question_1}**\n`{app_question_1}`\n**{question_2}**\n`{app_question_2}`\n**{question_3}**\n`{app_question_3}`\n**{question_4}**\n`{app_question_4}`\n**{question_5}**\n`{app_question_5}`\n**{question_6}**\n`{app_question_6}`\n**Статус:** `Открыта`", colour = discord.Colour.dark_gray())
                embed.set_footer(text = f"Дата: {time}")
                embed.set_thumbnail(url=uav)
                msg = await channel_app.send(embed = embed)
                await msg.add_reaction("✅")
                await msg.add_reaction("⛔")

                self.application.update({"_id": author.id}, {"$set": {"message": msg.id}})

                embed = discord.Embed(description = f"**{app_question_2}**, твоя заявка на сервер **Chimekko** была отправлена на рассмотрение.", colour = discord.Colour.blurple())
                await author.send(embed = embed)
                
            else:
                return


def setup(client):
    client.add_cog(User(client))
