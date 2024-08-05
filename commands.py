import discord
from discord import app_commands

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

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
    print(serverList)
    await interaction.response.send_message(serverList)

#Add    
@tree.command(
    name = "add",
    description="add a server to pingbot"
)
async def first_command(interaction: discord.Interaction, message: str):
    newServers = message.split("")
    for l in newServers:
        dnsFile = open("dns_server_name.txt", 'a')
        IPFile = open("ip_server_name.txt", 'a')
        if l.find(".clarkson.edu"):
            dnsFile.write(l + "\n")
        if l.find("128.153.14"):
            IPFile.write(l + "\n")
        dnsFile.close()
        IPFile.close()
    await interaction.response.send_message("added!")

@tree.command(
    name = "hold",
    description = "hold on pinging all or one server"
)
async def second_command(interaction):
    await interaction.response.send_message("Bye!")
    
@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")

f = open("token.txt", "r") # token can be manually inserted as `TOKEN = <number>` 
token = f.readline().strip('\n')
client.run(token) 