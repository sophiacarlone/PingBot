#Sophia Carlone 1/19/24
#Bot for COSI server management

import discord
from discord.ext import tasks #will allow the bot to check every X minutes
from discord.ext import commands
# from discord import app_commands
import os

DNS_IP = "128.153.145.53"
MINUTES = 10 #change to how many minutes in between checks
CHANNEL = 1033616359235538987 #change to channel preference

#setting up discord client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


#ping tests (aka the BEEF of the code)
@tasks.loop(minutes = MINUTES)  
async def Pinging():
    channel = client.get_channel(CHANNEL)           
    
    #try DNS server first
    response = os.system("ping -c 1 " + DNS_IP)
    if response != 0:
        warning = " DNS is down!"
        await channel.send(warning)

        #if DNS is down, try the ip addresses
        try:
            with open("ip_server_name.txt", "r") as f:
                for line in f:
                    hostname = line.strip('\n')
                    response = os.system("ping -c 1 " + hostname) #`-c 1` means send one packet
                        
                    if response != 0:
                        warning = (f"{hostname} is down!")
                        await channel.send(warning)
        
        except FileNotFoundError:
            print("File 'ip_server_name.txt' not found.")
        except Exception as e:
            print(f"Error occurred while reading 'ip_server_name.txt': {e}")

        f.close() 
        
    #DNS server is up: use domain names (more helpful for those unfamiliar of ip address allocation in COSI)
    else:
        try:                
            with open("dns_server_name.txt", "r") as f:
                for line in f:
                    hostname = line.strip('\n')
                    response = os.system("ping -c 1 " + hostname) 
                    
                    if response != 0:
                        warning = (f"{hostname} is down!") 
                        await channel.send(warning)                
        
        except FileNotFoundError:
            print("File 'dns_server_name.txt' not found.")
        except Exception as e:
            print(f"Error occurred while reading 'dns_server_name.txt': {e}")
        
        f.close()
        

def CommandListening():
    print("hit\n")
    
    
    
@client.event
async def on_ready(): #start of bot 
    # print(f'We have logged in as {client.user}')
    Pinging.start()
    CommandListening()

f = open("token.txt", "r") # token can be manually inserted as `TOKEN = <number>` 
token = f.readline().strip('\n')
client.run(token) 

# Suggestions:
# Control which servers Pingbot pings by adding them into dns_server_name.txt and ip_server_name.txt
# Possibility of using and parsing information from Zones repo, but clean up in the repo should be done first



############GARBAGE#############
# bot = commands.Bot(command_prefix = '$', intents = intents)
# @bot.command()
# async def test(ctx, arg):
#     print("hit\n")
#     await ctx.send("hi")


# tree = app_commands.CommandTree(client)
# client.tree = tree

# tree.command(name="echo", description="Echoes a message.")
# @app_commands.describe(message="The message to echo.")
# async def echo(interaction: discord.Interaction, message: str) -> None:
#     await interaction.response.send_message("thanks")