import discord
import json
from discord.ext import commands

with open('config.json', 'r') as file:
	config = json.load(file)

class User(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):   
        try:
            if after.channel.id == config["voice_channel"]["id_channel"]:
                maincategori = discord.utils.get(member.guild.categories, id = config["voice_channel"]["id_category"])
                channel2 = await member.guild.create_voice_channel(name = f'Приватка', category = maincategori)
                await channel2.set_permissions(member, connect = True, mute_members = True, move_members = True, manage_channels = True)
                await member.move_to(channel2)
                
                def check(x, y ,z):
                    return len(channel2.members) == 0
                await self.client.wait_for('voice_state_update', check=check)
                await channel2.delete()
                
        except:
            return

def setup(client):
    client.add_cog(User(client))