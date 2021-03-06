import discord
import json
import datetime
from discord.ext import commands
from pymongo import MongoClient

with open('config.json', 'r') as file:
	config = json.load(file)

class User(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.cluster = MongoClient("mongodb+srv://Bloodycat:PN1gkXf8H6Yf5X1P@chimekko-cluster.imrbn.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        self.application = self.cluster.Chimekko_db.application

    @commands.Cog.listener()
    async def on_member_join(self, member):
        application_in_bd = {"_id": member.id, "number": 0}
        if self.application.count_documents({"_id": member.id}) == 0:
            self.application.insert_one(application_in_bd)
        
        guild = member.guild
        datecreate = member.created_at.timestamp()
        date = datetime.datetime.now().strftime("%Y.%m.%d в %H.%M")
        try:
            createtime = int((datetime.datetime.now().timestamp() - datecreate) / (60*60*24))
            channel = self.client.get_channel(config['join']['id_channel'])
            embed = discord.Embed(description = f"{member.mention} зашел на сервер!\nВ дискорде: `{createtime}` дн.\nНа сервере: `{guild.member_count}` уч.", colour=discord.Colour.blue())
            embed.set_footer(text = f"Дата: {date}", icon_url=member.avatar_url)
            await channel.send(embed=embed)
            
        except:
            return

def setup(client):
    client.add_cog(User(client))