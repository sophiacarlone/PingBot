# This example requires the 'message_content' intent.

from discord.ext import tasks
import discord
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@tasks.loop(minutes=10.0)  # 10 minutes
async def pinging():
    #TODO: have dns its own special thing
    #TODO: all the servers
    hostname = "google.com" #example
    response = os.system("ping -c 1 " + hostname)
    if response == 0:
        print("still running")
    if response != 0:
        print(f"{hostname} is down!")
        warning = (f"{hostname} is down!")
        
        for guild in client.guilds:
            await guild.system_channel.send(warning)
 
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    pinging.start()

f = open("token.txt", "r")
token = f.readline().strip('\n')
client.run(token) 