import discord
import os
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
load_dotenv()
server_developers_den = os.getenv("TOKEN")  # Replace with your server ID
botid = os.getenv("BOTID")

#interact with user
class Client(commands.Bot):
    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})! \n This is for test ")
        
        try:
            guild = discord.Object(id=server_developers_den)
            synced = await self.tree.sync(guild = guild)
            print(f"Synced {len(synced)} commands to guild {guild.id}")
        except Exception as e:
            print(f"Error syncing commands: {e}")

    async def on_message(self,message):
        if message.author == self.user:
            return 
        
        if message.content.startswith("!hello"):
            await message.channel.send(f"Hello {message.author.mention}!")
            
    async def bot_reaction_add(self, reaction, user):
        if user.bot:
            return 
        guild = reaction.message.guild
        
        if not guild:
            return
        
        if hasattr(self, "colour_role_message_id") and reaction.message.id != self.colour_role_message_id:
            return 
        
        emoji = str(reaction.emoji)
        reaction_role_map = {'❤': 'Role',
                            '🤪': 'Role1'}
        
        if emoji in  reaction_role_map:
            role_name = reaction_role_map[emoji]
            role = discord.utils.get(guild.roles, name = role_name)
            
            if role and user:
                await user.add_roles(role)
                print(f"Assigned {role_name} to {user}")
                
                
    async def bot_reaction_remove(self, reaction, user):
        if user.bot:
            return 
        guild = reaction.message.guild
        
        if not guild:
            return
        
        if hasattr(self, "colour_role_message_id") and reaction.message.id != self.colour_role_message_id:
            return 
        
        emoji = str(reaction.emoji)
        reaction_role_map = {'❤': 'Role',
                            '🤪': 'Role1'}
        
        if emoji in  reaction_role_map:
            role_name = reaction_role_map[emoji]
            role = discord.utils.get(guild.roles, name = role_name)
            
            if role and user:
                await user.remove_roles(role)
                print(f"Assigned {role_name} to {user}")
            
            
    async def on_reaction_add(self,reaction,user):
        if user == self.user:
            return 
        
        if reaction.emoji == "👋":
            await reaction.message.channel.send(f"{user.mention} waved hello!")

intents=discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True  
intents.guilds = True 
client = Client(command_prefix="!" , intents=intents)


GUILD_ID = discord.Object(id = server_developers_den)

@client.tree.command(name="colorroles", description="pick a color", guild=GUILD_ID)
async def colour_roles(interaction: discord.Interaction):
    #check admin
    member = interaction.user
    if not isinstance(member, discord.Member):
        if interaction.guild is not None:
            member = await interaction.guild.fetch_member(interaction.user.id)
        else:
            await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)
            return
    if not member.guild_permissions.administrator:
        await interaction.response.send_message("Must be admin to assign roles", ephemeral=True)
        return 
    
    await interaction.response.defer(ephemeral=True)
    
    description = ("😊some emoji added here with text ")
    embed = discord.Embed(title="Pick color", description=description, color=discord.Color.blurple())
    message = await interaction.channel.send(embed=embed)
    emojis = ['👏','😒','😁','😜']
    
    for emoji in emojis:
        await message.add_reaction(emoji)
    
    client.colour_role_message_id = message.id
    
    await interaction.followup.send("color role created!", ephemeral=True)


#welcome opeartion
@client.tree.command(name="hello" , description="Says Hello to the user" , guild = GUILD_ID)
async def Greet(interaction: discord.Interaction):
    await interaction.response.send_message("Hello!")


@client.tree.command(name="receive" , description="input received" , guild = GUILD_ID)
async def printer(interaction: discord.Interaction, printer: str):
    await interaction.response.send_message(f"Received: {printer}")

#reply or mention opeartion
@client.tree.command(name="desc" , description="show test description" , guild = GUILD_ID)
async def descbox(interaction: discord.Interaction):
    embed = discord.Embed(title="test title" ,
                        url = "" ,
                        description = "test description",
                        color = discord.Color.red())
    embed.set_thumbnail(url="")
    embed.add_field(name="field 1" , value="", inline=True)
    embed.add_field(name="field 2" , value="", inline=True)
    embed.set_footer(text="this is footer")
    embed.set_author(name=interaction.user.name ,url="",icon_url=interaction.user.avatar.url) #add url=""
    await interaction.response.send_message(embed = embed)


#button opeartion
class View(discord.ui.View):
    @discord.ui.button(label = "Click me!" , style = discord.ButtonStyle.red, emoji=None)
    async def button_callback(self, button , interaction):
        await button.response.send_message("You clicked the button!")
        
        
    @discord.ui.button(label = "2nd button" , style = discord.ButtonStyle.blurple, emoji=None)
    async def button_callback1(self, button , interaction):
        await button.response.send_message("Second button clicked")
        
        
    @discord.ui.button(label = "3rd button" , style = discord.ButtonStyle.green, emoji=None)
    async def button_callback2(self, button , interaction):
        await button.response.send_message("third button clicked")
        
@client.tree.command(name="buttons" , description="show test buttons" , guild = GUILD_ID)
async def buttons(interaction: discord.Interaction):
    await interaction.response.send_message(view=View())
    
    
#drop down menu operation
class Menu(discord.ui.Select):
    def __init__(self):
        options = [discord.SelectOption(label="option 1", description="desc of option 1"), # can add emoji = " "
                discord.SelectOption(label="option 2", description="desc of option 2"),
                discord.SelectOption(label="option 3", description="desc of option 3")]
        
        super().__init__(placeholder="Choose an option", min_values=1,max_values=1, options=options)
        
    async def callback(self, interaction: discord.Interaction):
        if(self.values[0] == "option 1"):
            await interaction.response.send_message(f"you picked {self.values[0]}")
            
        if(self.values[0] == "option 2"):
            await interaction.response.send_message(f"you picked {self.values[1]}")
            
        if(self.values[0] == "option 3"):
            await interaction.response.send_message(f"you picked {self.values[2]}")
        
class menuview(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(Menu())
        
@client.tree.command(name="menu" , description="display drop down menu" , guild = GUILD_ID)
async def menu(interaction: discord.Interaction):
    await interaction.response.send_message(view=menuview())



client.run(botid)
