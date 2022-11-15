import discord, json
from discord.commands import slash_command,  SlashCommandGroup
from discord.commands import Option
from discord.ext import commands
from assist.database import database
import random


class MyMod(commands.Cog):
    """A category related server feedback and complaint"""
    def __init__(self, client):
        self.client = client

    @commands.command(name="mail")
    async def old_mail(self,ctx,*,query):
        await self._mail(ctx,query)

    @slash_command(name="mail")
    async def slash_mail(self,ctx,*,query):
        await self._mail(ctx,query)
    
    async def _mail(self,ctx,query):
        """Mail mods suggestions and feedback or questions. Be cautious before you disturb your mods :)"""
        id = ctx.guild.id
        server = database.getdata("server",id,database.DEFAULT_SERVER)
        if "mod_mod_channel" in server:
            mod_channel = server["mod_mod_channel"]
            mod_channel = ctx.guild.get_channel(mod_channel)
            e = discord.Embed(title=f"By {ctx.message.author.name}",description=query)
            
            await mod_channel.send(embed = e)
            try: await ctx.respond("Response Sent")
            except: await ctx.send("Response Sent")
        else:
            try: await ctx.respond("This server is not using MyMod, Pathetic! Set a mod channel to start")
            except: await ctx.send("This server is not using MyMod, Pathetic! Set a mod channel to start")

    
    slash_mod_channel = SlashCommandGroup("mod_channel", "Commands related mod_channel") 

    @commands.group(name="mod_channel",invoke_without_command=True)
    async def old_mod_channel(self,ctx):
        """Set/Get information about mod_channel used for MyMod System"""
        await ctx.send("Set/Get information about mod_channel used for MyMod System")

    @commands.has_permissions(moderate_members= True)
    @old_mod_channel.command(name="set")
    async def old_mod_mod_channel_set(self,ctx,*,mod_channel:discord.TextChannel):
        """Set a mod_channel for MyMod Service(Use probably slash commands)"""
        await self._mod_mod_channel_set(ctx,mod_channel)

    @commands.has_permissions(moderate_members= True)
    @slash_mod_channel.command(name="set")
    async def slash_mod_mod_channel_set(self,ctx,*,mod_channel:discord.TextChannel):
        """Set a mod_channel for MyMod Service"""
        await self._mod_mod_channel_set(ctx,mod_channel)

    async def _mod_mod_channel_set(self,ctx,mod_channel):
        id = ctx.guild.id
        database.savedata("server",id,{"mod_mod_channel":mod_channel.id})
        try: await ctx.respond(f"Successfully changed Mod mod_channel for MyMod Service to `{mod_channel.name}`")
        except: await ctx.send(f"Successfully changed Mod mod_channel for MyMod Service to `{mod_channel.name}`")

    @old_mod_channel.command(name="get")
    async def old_mod_mod_channel_get(self,ctx):
        """Know whats the mod_channel used for MyMod Service"""
        await self._mod_mod_channel_get(ctx)

    @slash_mod_channel.command(name="get")
    async def slash_mod_mod_channel_get(self,ctx):
        """Know whats the mod_channel used for MyMod Service"""
        await self._mod_mod_channel_get(ctx)

    async def _mod_mod_channel_get(self,ctx):
        id = ctx.guild.id
        server = database.getdata("server",id,database.DEFAULT_SERVER)
        if "mod_mod_channel" in server:
            mod_channel = server["mod_mod_channel"]
            mod_channel = ctx.guild.get_channel(mod_channel)
            try: await ctx.respond(f"ModChannel for MyMod Service is set to `{mod_channel.name}`")
            except: await ctx.send(f"ModChannel for MyMod Service is set to `{mod_channel.name}`")
        else:
            try: await ctx.respond(f"ModChannel for MyMod Service is not yet set")
            except: await ctx.send(f"ModChannel for MyMod Service is not yet set")

def setup(client):
    client.add_cog(MyMod(client))
    
