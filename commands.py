import discord
from discord import app_commands

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(
    name="commandname",
    description="My first application Command"
)
async def first_command(interaction):
    await interaction.response.send_message("Hello!")
    
@client.event
async def on_ready():
    await tree.sync()
    print("Ready!")

f = open("token.txt", "r") # token can be manually inserted as `TOKEN = <number>` 
token = f.readline().strip('\n')
client.run(token) 