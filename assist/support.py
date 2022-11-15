import discord
async def send_message(client,type:str="support",embed:discord.Embed=None):
    if type == "support": channel_id = 1041909940572405874
    elif type == "info": channel_id = 1041909940572405874
    else: print("Failed")
    channel = client.get_channel(channel_id)
    await channel.send(embed=embed)

    