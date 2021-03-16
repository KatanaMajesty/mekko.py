import discord
from discord.ext import commands
from pymongo import MongoClient
import json

with open('config.json', 'r') as file:
	config = json.load(file)

class User(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cluster = MongoClient("mongodb+srv://Bloodycat:PN1gkXf8H6Yf5X1P@chimekko-cluster.imrbn.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        self.tc = self.cluster.Chimekko_db.tc

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = discord.utils.find(lambda g: g.id == payload.guild_id, self.client.guilds)
        author = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)

        if author.bot:
            return

        message_id = payload.message_id
        if message_id == config["TC"]["id_message"]:
            if self.tc.count_documents({"_id": guild.id}) == 0:
                author_create = {"_id": guild.id, f"{author.id}": author.name}
                self.tc.insert_one(author_create)

            else:
                self.tc.update({"_id": guild.id}, {"$set": {f"{author.id}": author.name}})

            bot = guild.get_member(config["settings"]["id"])
            embed = discord.Embed(description = f"Вы подписались на объявления ТЦ 'Aqua'", color = 0xe6fff8)
            embed.set_thumbnail(url = bot.avatar_url)
            await author.send(embed = embed)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = discord.utils.find(lambda g: g.id == payload.guild_id, self.client.guilds)
        author = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)

        if author.bot:
            return

        message_id = payload.message_id
        if message_id == config["TC"]["id_message"]:

            self.tc.update({"_id": guild.id}, {"$unset" : {f"{author.id}" : 1 }}) 
            self.tc.update({"_id": guild.id}, {"$pull" : {f"{author.id}": 1}})

            bot = guild.get_member(config["settings"]["id"])
            embed = discord.Embed(description = f"Вы отменили подписку на объявления ТЦ 'Aqua'", color = 0xff4700)
            embed.set_thumbnail(url = bot.avatar_url)
            await author.send(embed = embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == config["TC"]["id_channel"]:
            member_tc = self.tc.find_one({"_id": message.guild.id})
            for members in member_tc:
                if members == "_id":
                    continue
                bot = message.guild.get_member(config["settings"]["id"])
                member = message.guild.get_member(int(members))
                embed = discord.Embed(description = f"**В канале ТЦ 'Aqua' новое объявление!**\n\nПросмотреть - <#{config['TC']['id_channel']}>", color = 0xe6fff8)
                embed.set_thumbnail(url = bot.avatar_url)
                await member.send(embed = embed)


def setup(client):
    client.add_cog(User(client))