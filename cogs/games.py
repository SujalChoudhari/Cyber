import random
import asyncio
from discord.ext import commands
from discord.commands import slash_command

class Game(commands.Cog):
    """Play various Games"""

    def __init__(self, bot):
        self.bot = bot


    @slash_command(name="8ball")
    async def slash_eight_ball(self,ctx,question:str):
        await self._eight_ball(ctx, question)
    
    @commands.command(name="8ball")
    async def old_eight_ball(self, ctx, ques=""):
        """Magic 8Ball"""
        await self._eight_ball(ctx, ques)

    async def _eight_ball(self,ctx,ques=""):
        if ques=="":
            await ctx.send("Ask me a question first")
        else:
            choices = [
            'It is certain.', 'It is decidedly so.', 'Without a doubt.', 'Yes – definitely.', 'You may rely on it.',
            'As I see it, yes.', 'Most likely.', 'Outlook good.', 'Yes.', 'Signs point to yes.',
            'Reply hazy, try again.', 'Ask again later.', 'Better not tell you now.', 'Cannot predict now.', 'Concentrate and ask again.',
            "Don't count on it.", 'My reply is no.', 'My sources say no.', 'Outlook not so good.', 'Very doubtful.'
            ]
            try: await ctx.respond(f":8ball: says: ||{random.choice(choices)}||")
            except: await ctx.send(f":8ball: says: ||{random.choice(choices)}||")


    @commands.command(name='rps', aliases=['rockpaperscissors'])
    async def rps(self, ctx):
        """Play Rock, Paper, Scissors game"""
        def check_win(p, b):
            if p=='🌑':
                return False if b=='📄' else True
            if p=='📄':
                return False if b=='✂' else True
            # p=='✂'
            return False if b=='🌑' else True

        async with ctx.typing():
            reactions = ['🌑', '📄', '✂']
            try: game_message = await ctx.respond("**Rock Paper Scissors**\nChoose your shape:", delete_after=15.0)
            except: game_message = await ctx.send("**Rock Paper Scissors**\nChoose your shape:", delete_after=15.0)
            for reaction in reactions:
                await game_message.add_reaction(reaction)
            bot_emoji = random.choice(reactions)

        def check(reaction, user):
            return user != self.bot.user and user == ctx.author and (str(reaction.emoji) == '🌑' or '📄' or '✂')
        try:
            reaction, _ = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
        except asyncio.TimeoutError:
            try: await ctx.respond("Time's Up! :stopwatch:")
            except: await ctx.send("Time's Up! :stopwatch:")
        else:
            await ctx.send(f"**:man_in_tuxedo_tone1:\t{reaction.emoji}\n:robot:\t{bot_emoji}**")
            # if conds
            if str(reaction.emoji) == bot_emoji:
                try: await ctx.respond("**It's a Tie :ribbon:**")
                except: await ctx.send("**It's a Tie :ribbon:**")
            elif check_win(str(reaction.emoji), bot_emoji):
                try: await ctx.respond("**You win :sparkles:**")
                except: await ctx.send("**You win :sparkles:**")
            else:
                try: await ctx.respond("**I win :robot:**")
                except: await ctx.send("**I win :robot:**")

        

    


    
    @slash_command(name="teams")
    async def slash_teams(self, ctx, num:int=2):
        """Makes random teams with specified number"""
        await self._teams(ctx,num=2)
    
    @commands.command(name='teams', aliases=['team'])
    async def old_teams(self, ctx, num:int=2):
        """Makes random teams with specified number"""
        await self._teams(ctx,num=2)

    
    async def _teams(self, ctx, num=2):
        if not ctx.author.voice:
            return await ctx.send("You are not connected to a voice channel :mute:")
        members = ctx.author.voice.channel.members
        memnames = []
        for member in members:
            memnames.append(member.name)

        remaining = memnames
        if len(memnames)>=num:
            for i in range(num):
                team = random.sample(remaining,len(memnames)//num)
                remaining = [x for x in remaining if x not in team]
                try: await ctx.respond(f"Team {chr(65+i)}\n" + "```CSS\n" + '\n'.join(team) + "\n```")
                except: await ctx.send(f"Team {chr(65+i)}\n" + "```CSS\n" + '\n'.join(team) + "\n```")
        if len(remaining)> 0:
            try: await ctx.respond("Remaining\n```diff\n- " + '\n- '.join(remaining) + "\n```")
            except: await ctx.send("Remaining\n```diff\n- " + '\n- '.join(remaining) + "\n```")


    @slash_command(name="toss")
    async def slash_toss(self, ctx):
        """Flips a Coin"""
        await self._toss(ctx)
    
    @commands.command(name='toss', aliases=['flip'])
    async def old_toss(self, ctx):
        """Flips a Coin"""
        await self._toss(ctx)
        
    async def _toss(self, ctx):
        coin = ['heads', 'tails']
        try: await ctx.respond(f"```diff\n{random.choice(coin)}\n```")
        except: await ctx.send(f"```diff\n{random.choice(coin)}\n```")

    

def setup(bot):
    bot.add_cog(Game(bot))