import discord, json
from discord.commands import slash_command
from discord.commands import Option
from discord.ext import commands


class Updates(commands.Cog):
    """A Category for Updates related to Bot """
    def __init__(self, client):
        self.client = client

    @slash_command(name = "logs",description = "Get updates of the development of Bot")
    async def slash_changelog(self,ctx,id:Option(int,"Enter the Id of a log to view it in detail",required = False,default = None)):
        await self._changelog(ctx, id)

    @commands.command(name = "logs",description = "Get updates of the development of Bot")
    async def old_changelog(self,ctx,id:int=None):
        await self._changelog(ctx, id)

    
    async def _changelog(self,ctx,id):
        with open("data/changelog.json")as f:
            logs = json.load(f)
        if id == None:
            e = discord.Embed(title=str(self.client.user) + " Changlogs")
            i = 0
            for log in logs:
                i +=1
                e.add_field(name=f"{i}. {logs[log]['title']}",value="version: "+log,inline=False)
                
            try: await ctx.respond(embed=e, ephemeral=True )
            except: await ctx.send(embed=e)
        else:
            id -=1
            try:
                #get correct log
                logs = logs[list(logs.keys())[id]]
                e = discord.Embed(title=logs['title'],description=logs['desc'])

                for name in logs['fields']:
                    e.add_field(name=name,value=logs['fields'][name])
                
                try: await ctx.respond(embed=e, ephemeral= True)
                except: await ctx.send(embed=e)
                    
            except IndexError:
                e = discord.Embed(
                        title="Out of Logs",
                        description="I searched long and hard, but the point is, my developers are lazy so there are not many changelogs"
                    )
                try: await ctx.respond(embed=e)
                except: await ctx.send(embed=e)

def setup(client):
    client.add_cog(Updates(client))
    
