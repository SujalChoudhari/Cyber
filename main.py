from assist.keep_alive import keep_alive
from assist import support
import discord
from discord.ext import commands
from pretty_help import PrettyHelp
import asyncio
import os

prefix = "//"
description = f"""[Invite](https://discord.com/api/oauth2/authorize?client_id=848090367022727179&permissions=8&scope=bot%20applications.commands)
use `{prefix}help [category]` or `{prefix}help [command]` to get more information about the category.
"""

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = commands.Bot(
    command_prefix=commands.when_mentioned_or(prefix),
    description=description,
    intents=intents,
)

client.avatar_url = "https://cdn.discordapp.com/avatars/848090367022727179/bf59aea0f9c2004f8561b3fe293d1b8c.webp?size=80"
client.author_id = 781767296121176074

ending_note = "{ctx.bot.user.name} @NotSujal#8873"

client.help_command = PrettyHelp(ending_note=ending_note)

@client.event
async def on_ready():
    print(f"\n\nLogged in as {client.user}\n\n")

    e = discord.Embed(title="Cyber Started!",
                      description="Cyber is up and running...")

    await support.send_message(client, "info", e)


for filename in os.listdir('./cogs'):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

keep_alive()
try:
    client.run(os.environ['TOKEN'])
except Exception as e:
    print(f"!!{e}!!")
    while True:
        pass
