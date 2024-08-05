#Sophia Carlone

import discord
from discord import app_commands
import time

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


##COMMANDS##

# List
@tree.command(
    name="list",
    description="list addresses to be pinged"
)
async def list(interaction):
    serverList = ""

    try:
        with open("dns_server_name.txt", "r") as f:
            for line in f:
                serverList += line                
    except FileNotFoundError:
        print("File 'dns_server_name.txt' not found.")
    except Exception as e:
        print(f"Error occurred while reading 'dns_server_name.txt': {e}")    
    f.close()

    try:
        with open("ip_server_name.txt", "r") as f:
            for line in f:
                serverList += line                
    except FileNotFoundError:
            print("File 'ip_server_name.txt' not found.")
    except Exception as e:
            print(f"Error occurred while reading 'ip_server_name.txt': {e}")    
    f.close()

    await interaction.response.send_message(serverList)


#Add    
@tree.command(
    name = "add",
    description="add a server to pingbot"
)
async def first_command(interaction: discord.Interaction, message: str):
    newServers = message.split(" ")
    dnsFile = open("dns_server_name.txt", 'a')
    IPFile = open("ip_server_name.txt", 'a')

    for l in newServers:
        if l.find(".clarkson.edu") != -1:
            dnsFile.write(l + "\n")
        if l.find("128.153.14") == 0:
            IPFile.write(l + "\n")

    dnsFile.close()
    IPFile.close()
    await interaction.response.send_message("added!")


#Hold
@tree.command(
    name = "hold",
    description = "hold on pinging servers"
)
async def second_command(interaction):
    sleep(86400) #86400 for 24 hrs
    await interaction.response.send_message("Holding for 24 hours")


#Start up    
@client.event
async def on_ready():
    await tree.sync()

f = open("token.txt", "r") # token can be manually inserted as `TOKEN = <number>` 
token = f.readline().strip('\n')
client.run(token) 