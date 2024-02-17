#Sophia Carlone 1/19/24
#Bot for COSI server management

from discord.ext import tasks #will allow the bot to check every X minutes
import discord
import os

DNS_IP = "128.153.145.53"
DNS = True

#setting up discord client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@tasks.loop(minutes=10.0)  # 10 minutes
async def pinging():
    channel = client.get_channel(1033616359235538987)  # sys-admin channel         
    
    #try dns first
    response = os.system("ping -c 1 " + DNS_IP)
    if response != 0:
        warning = " DNS is down!"
        await channel.send(warning)
        print("HITS")
        DNS = False
        #if DNS is down, try the ip addresses
     
    if not dns:   
        print("hello")
        try:
            with open("ip_server_name.txt", "r") as f:
                for line in f:
                    hostname = line.strip('\n')
                    response = os.system("ping -c 1 " + hostname)
                        
                    if response == 0:
                        await channel.send(f"{hostname} ip worked.")
                    else:
                        warning = (f"{hostname} is down!")
                        await channel.send(warning)
        
        except FileNotFoundError:
            print("File 'ip_server_name.txt' not found.")
        except Exception as e:
            print(f"Error occurred while reading 'ip_server_name.txt': {e}")
        
        # with open("ip_server_name", "r") as f: #line with all ip addresses (could make a webhook later to automatically pull from zones)
        #         print("hit c")
        #         for line in f:
        #             print("hit A")
        #             hostname = line.strip('\n')
        #             response = os.system("ping -c 1 " + hostname)
                    
        #             #could use a try catch, but nah
        #             if response == 0:
        #                 await channel.send(f"{hostname} ip worked.")
                
        #             else:
        #                 warning = (f"{hostname} is down!")
        #                 await channel.send(warning)
        f.close() 
        
    #dns is up, so try those entries
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
     
@client.event
async def on_ready():
    # print(f'We have logged in as {client.user}')
    pinging.start()

f = open("token.txt", "r")
token = f.readline().strip('\n')
client.run(token) 