#Sophia Carlone 1/19/24
#Bot for COSI server management

from discord.ext import tasks
import discord
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@tasks.loop(minutes=10.0)  # 10 minutes
async def pinging():
    dns = False
    #try dns first
    with open("dns_server_name.txt", "r") as f:
        for line in f:
            hostname = line.strip('\n')
            response = os.system("ping -c 1 " + hostname)
            
            if response == 0:
                # print("still running")
                dns = True
                # for guild in client.guilds:
                #     await guild.system_channel.send("everything is running smoothly")
            
            if response != 0:
                # print(f"{hostname} is down!")
                warning = (f"{hostname} is down!")
                
                for guild in client.guilds:
                    await guild.system_channel.send(warning)
    f.close()
                
    if(not dns):
        for guild in client.guilds:
            await guild.system_channel.send("May be a dns issue. Trying IP addressess now")
            
        with open("ip_server_name", "r") as f:
            for line in f:
                hostname = line.strip('\n')
                response = os.system("ping -c 1 " + hostname)
                
                if response == 0:
                    for guild in client.guilds:
                        await guild.system_channel.send(f"{hostname} ip worked.")
            
                if response != 0:
                    # print(f"{hostname} is down!")
                    warning = (f"{hostname} is down!")
                
                    for guild in client.guilds:
                        await guild.system_channel.send(warning)
    f.close()
            
 
@client.event
async def on_ready():
    # print(f'We have logged in as {client.user}')
    pinging.start()

f = open("token.txt", "r")
token = f.readline().strip('\n')
client.run(token) 