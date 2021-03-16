import discord
import json
import datetime
from discord.ext import commands

with open('config.json', 'r') as file:
	config = json.load(file)

class User(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = message.channel

        if channel.id != config['moderatoin']['id_channel_screen']:
            return
        if not message.attachments:
            await message.channel.purge(limit = 1)
            return
        

def setup(client):
    client.add_cog(User(client))