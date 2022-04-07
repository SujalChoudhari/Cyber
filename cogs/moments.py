from discord.ext import commands
import discord
from discord.utils import get
from discord.commands import slash_command

class starboard(commands.Cog, name="Star Board"):
    """ A Category for Global StarBoard Commands"""
    def __init__(self,client):
        self.client = client

    @slash_command(name="moments")
    async def slash_moments(self,ctx):
        await self._moments(ctx) 
        
    @commands.command(name="moments" )
    async def old_moments(self,ctx):
        await self._moments(ctx)

        
    async def _moments(self,ctx):

        text= """
        Now connect with other servers globally, get best moments from other servers.

        > __To receive global posts__, your server should have a #cyber-moments channel and the bot should have permissions to send messages.

        > __To send messages to cyber-moments__, react the message with "⬆️". A message should have more than 5 reactions to make it to cyber-moments

        """

        e = discord.Embed(title = "** CyberMoments **",description=text)
        
        try: await ctx.respond(embed = e, ephemeral= True)
        except: await ctx.send(embed = e)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        if payload.emoji.name == '⬆️':
            guild = await self.client.fetch_guild(payload.guild_id)
            channel = self.client.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            reaction = get(message.reactions, emoji=payload.emoji.name)


            if reaction  and reaction.count >=4:
                for _guild in self.client.guilds:
                    for channel in _guild.channels:
                        if "cyber-moments" in channel.name:

                            e = discord.Embed(
                                title = f"⬆️ From: `{guild.name}`  By: `{message.author.name}` ",
                                description = message.content
                            )

                            for attach in message.attachments:
                                e.add_field(name="attachment:",value= attach.url)
                            await channel.send(embed = e)
def setup(client):
    client.add_cog(starboard(client))

