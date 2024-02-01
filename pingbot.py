#Sophia Carlone 1/19/24
#Bot for COSI server management

from discord.ext import tasks #will allow the bot to check every X minutes
import discord
import os

#setting up discord client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@tasks.loop(minutes=10.0)  # 10 minutes
async def pinging():
    dns = False
    channel = client.get_channel(1064033255071957042)  #783047906550218792 sys-admin channel         
    
    #try dns first
    with open("dns_server_name.txt", "r") as f:
        for line in f:
            hostname = line.strip('\n')
            response = os.system("ping -c 1 " + hostname) #the -c 1 means that you are only sending one packet
            
            if response == 0:
                dns = True #dns is seemingly working
            
            else:
                warning = (f"{hostname} is down!") 
                await channel.send(warning)
                    
    f.close()
     
     #no dns entry worked           
    if(not dns): 
        await channel.send("May be a dns issue. Trying IP addresses now")
            
        with open("ip_server_name", "r") as f:
            for line in f:
                print("hit")
                hostname = line.strip('\n')
                response = os.system("ping -c 1 " + hostname)
                
                #could use a try catch, but nah
                if response == 0:
                    await channel.send(f"{hostname} ip worked.")
            
                else:
                    warning = (f"{hostname} is down!")
                    await channel.send(warning)
                        
    f.close()
            
 
@client.event
async def on_ready():
    # print(f'We have logged in as {client.user}')
    pinging.start()

f = open("token.txt", "r")
token = f.readline().strip('\n')
client.run(token) 