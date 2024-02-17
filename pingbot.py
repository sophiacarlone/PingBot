#Sophia Carlone 1/19/24
#Bot for COSI server management

from discord.ext import tasks #will allow the bot to check every X minutes
import discord
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
async def pinging():
    channel = client.get_channel(CHANNEL)           
    
    #try dns first so that you go straight to IPS
    response = os.system("ping -c 1 " + DNS_IP)
    if response != 0:
        warning = " DNS is down!"
        await channel.send(warning)

        #if DNS is down, try the ip addresses
        try:
            with open("ip_server_name.txt", "r") as f:
                for line in f:
                    hostname = line.strip('\n')
                    response = os.system("ping -c 1 " + hostname)
                        
                    if response != 0:
                        warning = (f"{hostname} is down!")
                        await channel.send(warning)
        
        except FileNotFoundError:
            print("File 'ip_server_name.txt' not found.")
        except Exception as e:
            print(f"Error occurred while reading 'ip_server_name.txt': {e}")

        f.close() 
        
    #dns is up, so use domain names (more helpful for those who are unfamiliar which server has which ip address)
    else:
        try:                
            with open("dns_server_name.txt", "r") as f:
                for line in f:
                    hostname = line.strip('\n')
                    response = os.system("ping -c 1 " + hostname) #the -c 1 means that you are only sending one packet
                    
                    if response != 0:
                        warning = (f"{hostname} is down!") 
                        await channel.send(warning)                
        
        except FileNotFoundError:
            print("File 'ip_server_name.txt' not found.")
        except Exception as e:
            print(f"Error occurred while reading 'ip_server_name.txt': {e}")
        
        f.close()
    
    
#start of bot 
@client.event
async def on_ready():
    # print(f'We have logged in as {client.user}')
    pinging.start()

f = open("token.txt", "r")
token = f.readline().strip('\n')
client.run(token) 