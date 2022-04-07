import discord
from discord.ext import commands
from discord.commands import slash_command, SlashCommandGroup
from assist.database import database


class Welcomer(commands.Cog):
    """ A Category for Global StarBoard Commands"""
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        id = member.guild.id
        server = database.getdata("server", id, database.DEFAULT_SERVER)
        if server == None and not server['welcome_toggle']: return
        channel_id = server['welcome_channel']
        try:
            channel = self.client.get_channel(channel_id)
            e = discord.Embed(
                title=f"{member.name} Welcome!",
                description=
                f"Thanks for Joining, {member.name} you are an Absolute Legend!")

            e.set_thumbnail(
                url=f"{member.avatar.url}")
            e.set_footer(text="Hope You won't Leave :)")
            await channel.send(embed=e)
        except:
            pass

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        id = member.guild.id
        server = database.getdata("server", id, database.DEFAULT_SERVER)
        if server == None and not server['welcome_toggle']: return
        channel_id = server['welcome_channel']
        try:
            channel = self.client.get_channel(channel_id)
            e = discord.Embed(
                title=f"{member.name} just left!",
                description=
                f"Why do people spontaneously keep leaving??")

            e.set_footer(text="Anyways, hope you remember us, :sob: ")
            await channel.send(embed=e)
        except:
            pass

            
    # slash welcomer commands
    slash_welcomer = SlashCommandGroup("welcome", "Welcome System") 

    @slash_welcomer.command(name="channel")
    @commands.has_permissions(moderate_members=True)
    async def slash_welcomer_channel(self,ctx,channel_id=None):
        """Set/Get Welcome Channel"""
        await self._set_channel(ctx,channel_id)

    @slash_welcomer.command(name="on")
    @commands.has_permissions(moderate_members= True)
    async def slash_welcomer_on(self,ctx):
        """Enable Welcome System"""
        await self._welcomer_toggle(ctx, True)
        
    @slash_welcomer.command(name="off")
    @commands.has_permissions(moderate_members= True)
    async def slash_welcomer_off(self,ctx):
        """Disable Welcome System"""
        await self._welcomer_toggle(ctx, False)
    
            
    # old welcomer commands
    @commands.group(name="welcome", invoke_without_command=True)
    async def old_welcomer(self, ctx):
        """Setup welcomer Channels and Enable/Disable it [has subcommands] (Default: OFF)"""
        await ctx.send("welcome system, use `//help welcomer` to know about all the commands.")

    @old_welcomer.command(name="on")
    @commands.has_permissions(moderate_members=True)
    async def old_welcomer_on(self, ctx):
        """Enable Welcome System"""
        await self._welcomer_toggle(ctx, True)

    @old_welcomer.command(name="off")
    @commands.has_permissions(moderate_members=True)
    async def old_welcomer_off(self, ctx):
        """Disable Welcome System"""
        await self._welcomer_toggle(ctx, False)

    @old_welcomer.command(name="channel")
    @commands.has_permissions(moderate_members=True)
    async def old_welcomer_channel(self, ctx, channel_id=None):
        """Set Welcome Channel"""
        await self._set_channel(ctx,channel_id)

    async def _welcomer_toggle(self, ctx, toggle: bool):
        id = ctx.guild.id
        database.savedata("server", id, {"welcomer_toggle": toggle})
        if toggle: state = "Enabled"
        else: state = "Disabled"
        try:
            await ctx.respond(f"**Welcome System {state}**")
        except:
            await ctx.send(f"**Welcome System {state}**")

    async def _set_channel(self,ctx,channel_id=None):
        id = ctx.guild.id
        if channel_id == None:
            current_channel_id = database.getdata("server",id,database.DEFAULT_SERVER)
            if "welcome_channel" in current_channel_id:
                current_channel_id = current_channel_id["welcome_channel"]
            else:
                current_channel_id = 404
            if current_channel_id == 404:
                try: await ctx.respond("**Channel Id Not Yet Set**")
                except: await ctx.send("**Channel Id Not Yet Set**")
            else:
                try: await ctx.respond(f"**Current Weclome Channel is <#{current_channel_id}>**")
                except: await ctx.send(f"**Current Weclome Channel is <#{current_channel_id}>**")
            return
            
        database.savedata("server", id, {"welcome_channel": channel_id})
        try:await ctx.respond(f"**Welcome Channel Set**")
        except:await ctx.send(f"**Welcome Channel Set**")

def setup(client):
    client.add_cog(Welcomer(client))
