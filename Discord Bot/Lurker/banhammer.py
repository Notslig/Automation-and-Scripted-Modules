#MODERATION :-

import os
import discord
import sqlite3
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from keepalive import keepalive # to keep bot running 24/7 and prevent shutdown
keepalive()

dbDIR = os.path.dirname(os.path.abspath(__file__))   # set to storee db in this directory

load_dotenv()
AWICS = os.getenv("TOKEN")   # token is stored in this variable

intents = discord.Intents.default()
intents.message_content = True   # bot permission to message

bot = commands.Bot (command_prefix = "!", intents = intents )


# add this for recieving a profanity check on messages before the modeartion part (optional) in seperate bot file including the moderation
@bot.event
async def on_ready():
    await bot.tree.sync() # enable /commands

@bot.event
async def on_message(message):
    if bot.user is not None and message.author.id != bot.user.id:
        for term in illegalwords:
            if term.lower() in message.content.lower():
                warning = warning_count(message.author.id, message.guild.id)
                limit: int = 5
                if warning > limit:
                    await message.author.ban(reason = "Yo calm down with those words, anyway your getting Fox-3 'ed ")
                    await message.channel.send(f"{message.author.mention} has been AMRAAM'ed ")
                else:
                    await message.channel.send(f" {message.author.mention} has been pinged by {bot.user.id} {warning} times ") # check for bot.user.id for validation
                    await message.delete()
                break
    
    await bot.process_commands(message) # other commands process before continuing



illegalwords = ["nigga","nigger","cunt","job"]  # keep adding profanitites in the list

def warning_count(USERID: int , GUILDID: int):
    connectSQL = sqlite3.connect(f"{dbDIR}\\UsersModeration.db")
    cursor = connectSQL.cursor()
    cursor.execute("""select RADARPING from GUILD_USERS where (USERID = ?) and (GUILDID = ?) ;""", (USERID, GUILDID)) # replaces '?' in the query
    retrieve = cursor.fetchone() # retrieves one row cause of one user id
    
    # add RADARPING SETTINGS
    if retrieve == None:
        cursor.execute(""" insert into GUILD_USERS (USERID, GUILDID, RADARPING) values (?,?,1)) ; """,(USERID, GUILDID))
        connectSQL.commit()
        connectSQL.close()
        
        return 1

    cursor.execute(""" update GUILD_USERS set RADARPING = ? where ( USERID = ? ) and ( GUILDID = ? ) ; """, (retrieve[0] + 1, USERID, GUILDID))
    connectSQL.commit()
    connectSQL.close()
    
    return retrieve[0] + 1 #rtrieve should update to new details


    
    
    
def create_user_table():
    connectSQL = sqlite3.connect(f"{dbDIR}\\UsersModeration.db") #connect to DB and root file
    cursor = connectSQL.cursor() #make a cursor point
    
    cursor.execute("""
                create table if not exists "GUILD_USERS" (
                    "USERID" integer,
                    "GUILDID" integer,
                    "RADARPING" integer,
                    primary key("USERID","GUILDID")
                )
                """)
    connectSQL.commit()
    connectSQL.close()
    
create_user_table()


bot.run(" ") #replace the token variable