import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

dbDIR = os.path.dirname(os.path.abspath(__file__))   # set to storee db in this directory

load_dotenv()
token = os.getenv("TOKEN")   # token is stored in this variable

intents = discord.Intents.default()
intents.message_content = True   # bot permission to message

bot = commands.Bot (command_prefix = "!", intents = intents )


@bot.event
async def on_ready():
    await bot.tree.sync() # enable /commands
    print(f"{bot.user} is online and ready to engage!")  #just give a heads up when online
    
@bot.event
async def on_message(message):
    if bot.user is not None and message.author.id != bot.user.id:  #does not take bots message inro account
        await message.channel.send(f"Message has been recieved {message.author.mention}")  #SET TO WELCOMER FOR WELCOME MESSAGE
        
        
        
@bot.tree.command(name="message", description="acknowledges the message")
async def message(interaction: discord.Interaction):
    username = interaction.user.mention
    await interaction.response.send_message("Acknowledgement recieved {username}")  # /command for message
    

bot.run(" ") #replace the token variable