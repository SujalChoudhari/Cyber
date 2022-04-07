import discord
async def send_message(client,type:str="support",embed:discord.Embed=None):
    if type == "support": channel_id = 953134900939210802
    elif type == "info": channel_id = 953140964418007080
    else: print("Failed")
    channel = client.get_channel(channel_id)
    await channel.send(embed=embed)
    