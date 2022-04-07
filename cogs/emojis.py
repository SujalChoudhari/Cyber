import discord, json, requests
from discord.ext import commands
from discord.commands import slash_command, SlashCommandGroup
import asyncio,os
from assist.database import database
class Emoji(commands.Cog):
    """A Category for Emoji based commands"""
    
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self,msg):
        id = msg.guild.id
        server = database.getdata("server",id,database.DEFAULT_SERVER)
        if server == None or not server['emoji_toggle']: return
        apikey = os.environ['GIF_KEY']
        if msg.author.bot: return
        ipt  =msg.content 

        search_term = False
        with open("data/emoticons.json")as f:
            emojies = json.load(f)

        for key, value in emojies.items():
            for each in value:
                if each in ipt and not "http" in ipt:
                    search_term = key
        if search_term:
            r = requests.get(
        "https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, apikey, 1))
            if r.status_code == 200:
                # load the GIFs using the urls for the smaller GIF sizes
                gif = json.loads(r.content)
                image =await msg.channel.send(
                gif["results"][0]["media"][0]["nanogif"]["url"] )
            return
                
        if ipt.startswith(":"):
            search_term = ipt.replace(":","")
            r = requests.get(
        "https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, apikey, 1))
            if r.status_code == 200:
                # load the GIFs using the urls for the smaller GIF sizes
                gif = json.loads(r.content)
                image =await msg.channel.send(
                gif["results"][0]["media"][0]["nanogif"]["url"] )
                await asyncio.sleep(6)
                await image.edit(content= gif["results"][0]["media"][0]["mediumgif"]["url"] )

    # slash gifs commands
    slash_gifs = SlashCommandGroup("gif", "Gif system") 
    slash_gifs_manage = slash_gifs.create_subgroup("set", "Manage Gif system, Default is OFF")

    @slash_gifs.command(name="emoticons")
    async def slash_emojis(self,ctx):
        """Get a list of supported emoticons"""
        await self._emojis(ctx)

    @slash_gifs.command(name="send")
    async def slash_send_emoji(self,ctx,*,query):
        """Send an emoji to chat"""
        await self._send_emoji(ctx,query)

    @slash_gifs_manage.command(name="on")
    @commands.has_permissions(manage_emojis= True)
    async def slash_emoji_manage_on(self,ctx):
        """Toggle Gif System on"""
        await self._emoji_manage_toggle(ctx,True)
        
    @slash_gifs_manage.command(name="off")
    @commands.has_permissions(manage_emojis= True)
    async def slash_emoji_manage_off(self,ctx):
        """Toggle Gif System off"""
        await self._emoji_manage_toggle(ctx,False)
    
    # old gif commands
    @commands.group(name="gif",invoke_without_command=True)
    async def old_gifs(self,ctx):
        """Get info and manage gif system [has subcommands]"""
        await ctx.send("gif system, use `//help gif` to know about all the commands.")

    @old_gifs.command(name="emoticons")
    async def old_emojis(self,ctx):
        """Get a list of supported emoticons"""
        await self._emojis(ctx)

    @old_gifs.command(name="send")
    async def old_send_emoji(self,ctx,*,query):
        """Send an emoji to chat"""
        await self._send_emoji(ctx,query)

    # old manage commands
    @old_gifs.group(name="set",invoke_without_command=True)
    async def old_emoji_manage(self,ctx,toggle:str="on"):
        """Activate and Deactivate the Gif System, Server Owners Only. Default is off. """
        await ctx.send("gif system, use `//help gif set` to know about all the commands.")

    @old_emoji_manage.command(name="on")
    @commands.has_permissions(manage_emojis= True)
    async def old_emoji_manage_on(self,ctx):
        await self._emoji_manage_toggle(ctx,True)
        
    @commands.has_permissions(manage_emojis= True)
    @old_emoji_manage.command(name="off")
    async def old_emoji_manage_off(self,ctx):
        await self._emoji_manage_toggle(ctx,False)
    

    async def _emojis(self,ctx):
        with open("data/emoticons.json") as f:
            emoticons = json.load(f)
            e = discord.Embed(title="Supported Emoticons",description="Only few emoticons are supported")
            for keys in emoticons:
                val = ""
                for emo in emoticons[keys]:
                    val += emo + "  "
                e.add_field(name=keys,value=str(val))
    
        try: await ctx.respond(embed=e,ephemeral=True)
        except:await ctx.send(embed=e)

    async def _send_emoji(self,ctx,query):
        apikey = os.environ['GIF_KEY']
        r = requests.get(
        "https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (query, apikey, 1))
        if r.status_code == 200:
            # load the GIFs using the urls for the smaller GIF sizes
            gif = json.loads(r.content)
            try: await ctx.respond(gif["results"][0]["media"][0]["mediumgif"]["url"] )
            except: await ctx.send(gif["results"][0]["media"][0]["mediumgif"]["url"] )

    async def _emoji_manage_toggle(self,ctx,toggle:bool):
        #if not ctx.message.author.guild_permissions.manage_emojis:
            #try: await ctx.respond(f"You don't have `Manage Emojis` Permissions")
            #except: await ctx.send(f"You don't have `Manage Emojis` Permissions")
            #return
        id = ctx.guild.id
        database.savedata("server",id,{"emoji_toggle":toggle})
        if toggle: state = "Enabled"
        else: state = "Disabled"
        try: await ctx.respond(f"**Emoji System {state}**")
        except: await ctx.send(f"**Emoji System {state}**")
            
def setup(client):
    client.add_cog(Emoji(client))
    
