import json
from assist import support
import discord
from discord.ui import Button, View
from discord.ext import commands
from discord.commands import slash_command

class Misc(commands.Cog):
    """Miscellaneous Commands that no one uses"""
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True) 
    @commands.command(name='clear', aliases=['cls'])
    async def clear(self, ctx, limit=20):
        """Delete the messages sent in current text-channel"""
        if 1>limit>100:
            limit = 20
        try:
            await ctx.message.channel.purge(limit=limit)
        except discord.Forbidden:
            await ctx.send("I don't have permission to `Manage Messages`:disappointed_relieved:")

    @slash_command(name='help')
    async def help(self, ctx, detailed:bool=False):
        await ctx.respond("help  is not supported for slash commands, use `//help` instead")

        """Display help"""
        """embed = discord.Embed(title="Commands of Cyber", colour=discord.Colour(0x7f20a0))

        embed.set_footer(text="Cyber by NotSujal#8873✨")

        if detailed:
            # Full version
            embed.description = 'My prefix is `//`'
            with open('data/help.json', 'r') as help_file:
                data = json.load(help_file)
            data = data['full']
            for key in data:
                value = '\n'.join(x for x in data[key])
                embed.add_field(name=key, value=f"```{value}```", inline=False)
        else:
            # Short version
            embed.description = 'My prefix is `//`\nType.'
            with open('data/help.json', 'r') as help_file:
                data = json.load(help_file)
            data = data['short']
            for key in data:
                embed.add_field(name=key, value=data[key])
        try:
            await ctx.respond(embed=embed)
        except Exception:
            await ctx.respond("I don't have permission to send embeds here :disappointed_relieved:")
"""
    @commands.command(name='invite')
    async def old_invite(self,ctx):
        await self._invite(ctx)

    @slash_command(name="invite", description= "My Invite Link")
    async def slash_invite(self,ctx):
        await self._invite(ctx)
    
    async def _invite(self, ctx):
        """My invite link"""
        
        link = Button(label="Invite",style=discord.ButtonStyle.link,url="https://discord.com/api/oauth2/authorize?client_id=848090367022727179&permissions=8&scope=bot%20applications.commands")
        view = View()
        view.add_item(link)
        
        
        # e= discord.Embed(title="Invite",description= f"""[Link](https://discord.com/api/oauth2/authorize?client_id=848090367022727179&permissions=8&scope=bot%20applications.commands)""")
        try: await ctx.respond(view=view)
        except: await ctx.send(view=view)

    @commands.command(name='ping', aliases=['latency'])
    async def old_ping(self, ctx):
        """ Pong! """
        await self._ping(ctx)

    @slash_command(name="ping",description="Pong!")
    async def slash_ping(self, ctx):
        """ Pong! """
        await self._ping(ctx)

    
    async def _ping(self, ctx):
        try: message = await ctx.respond(":ping_pong: Pong!")
        except: message = await ctx.send(":ping_pong: Pong!")
        ping = (message.created_at.timestamp() - ctx.message.created_at.timestamp()) * 1000
        await message.edit(content=f":ping_pong: Pong!\nTook `{int(ping)}ms`\nLatency: `{int(self.bot.latency*1000)}ms`")
        
    @commands.cooldown(1, 3600, commands.BucketType.user)
    @commands.command(name='feedback',aliases=['support', 'contact'])
    async def contact(self, ctx, *, msg: str = ""):
        """Contact bot owner"""
        
        if len(msg) < 20:
            return await ctx.send("Please enter a message more than 20 characters to send towards Developers", delete_after=5.0)

        embed = discord.Embed(colour=discord.Colour(0x5dadec), title= f"{ctx.message.author.name}: {ctx.message.author.id}",description=msg)
        embed.set_footer(text=f"{ctx.guild} : {ctx.guild.id}")

        await support.send_message(self.bot, "support", embed)
        await ctx.send("Developers Notified!")

    @commands.command(name='tts')
    async def _tts(self, ctx, *, text=''):
        """Send tts message"""
        if not text:
            return await ctx.send('Specify message to send')
        await ctx.send(content=text, tts=True)
        
    @contact.error
    async def error_support(self,ctx, error):
        if isinstance(error, commands.CommandOnCooldown): 
            _time = int(error.retry_after)
            if _time > 60:
                time = str(int(_time /(60))) + " minutes"
            if _time <=  60: 
                time = str(_time) + " secs"
            em = discord.Embed(title=f"Slow it down bro!",description=f"Try again in {time}.")
            await ctx.send(embed=em)

    @commands.command(name='poll')
    async def quickpoll(self, ctx, question, *options: str):
        """Create a quick poll[~poll "question" choices]"""
        if len(options) <= 1:
            await ctx.send('You need more than one option to make a poll!')
            return
        if len(options) > 10:
            await ctx.send('You cannot make a poll for more than 10 things!')
            return

        if len(options) == 2 and options[0] == 'yes' and options[1] == 'no':
            reactions = ['✅', '❌']
        else:
            reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

        description = []
        for x, option in enumerate(options):
            description += '\n {} {}'.format(reactions[x], option)
        embed = discord.Embed(title=question, description=''.join(description), color=discord.Colour(0xFF355E))
        react_message = await ctx.send(embed=embed)
        for reaction in reactions[:len(options)]:
            await react_message.add_reaction(reaction)
        embed.set_footer(text='Poll ID: {}'.format(react_message.id))
        await react_message.edit(embed=embed)

    @commands.has_permissions(administrator=True) 
    @commands.command(name='tally')
    async def tally(self, ctx, pid):
        """Tally the created poll"""
        poll_message = await ctx.message.channel.fetch_message(pid)
        if not poll_message.embeds:
            return
        embed = poll_message.embeds[0]
        if poll_message.author != self.bot.user:
            return
        if not embed.footer.text.startswith('Poll ID:'):
            return
        unformatted_options = [x.strip() for x in embed.description.split('\n')]
        opt_dict = {x[:2]: x[3:] for x in unformatted_options} if unformatted_options[0][0] == '1' \
            else {x[:1]: x[2:] for x in unformatted_options}
        # check if we're using numbers for the poll, or x/checkmark, parse accordingly
        voters = [self.bot.user.id]  # add the bot's ID to the list of voters to exclude it's votes

        tally = {x: 0 for x in opt_dict.keys()}
        for reaction in poll_message.reactions:
            if reaction.emoji in opt_dict.keys():
                reactors = await reaction.users().flatten()
                for reactor in reactors:
                    if reactor.id not in voters:
                        tally[reaction.emoji] += 1
                        voters.append(reactor.id)

        output = 'Results of the poll for "{}":\n'.format(embed.title) + \
                '\n'.join(['{}: {}'.format(opt_dict[key], tally[key]) for key in tally.keys()])
        await ctx.send(output)


def setup(bot):
    bot.add_cog(Misc(bot))