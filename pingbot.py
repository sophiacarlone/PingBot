#Sophia Carlone 1/19/24
#Bot for COSI server management

##IMPORTS, CONSTANTS, GLOBAL VARIABLES, SETUP##
import os
import time
import discord
from discord.ext import tasks #will allow the bot to check every X minutes
from discord import app_commands


DNS_IP = "128.153.145.53"
MINUTES = 10 #change to how many minutes in between checks
CHANNEL = 1033616359235538987 #change to channel preference
SLEEP = 86400 #86400 for 24 hrs


#setting up discord client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


##FUNCTIONS##
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

    for l in newServers: #TODO check if server has already been entered (though, it wont affect results of pings)
        if l.find(".clarkson.edu") != -1:
            dnsFile.write(l + "\n")
        if l.find("128.153.14") == 0:
            IPFile.write(l + "\n")

    dnsFile.close()
    IPFile.close()
    await interaction.response.send_message("added!") #TODO more personalized message


#Hold
@tree.command(
    name = "hold",
    description = "hold on pinging servers"
)
async def second_command(interaction):
    sleep(SLEEP) 
    await interaction.response.send_message("Holding for 24 hours")
    


##MAIN##    
@client.event
async def on_ready(): #start of bot 
    # print(f'We have logged in as {client.user}')
    await tree.sync()
    Pinging.start()

f = open("token.txt", "r") # token can be manually inserted as `TOKEN = <number>` 
token = f.readline().strip('\n')
client.run(token) 


##SUGGESTIONS##
# Control which servers Pingbot pings by adding them into dns_server_name.txt and ip_server_name.txt
# Possibility of using and parsing information from Zones repo, but clean up in the repo should be done first