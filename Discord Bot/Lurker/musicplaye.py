#in dev mode set application.commands and bot on from perms
import os
import discord
import yt_dlp
import asyncio
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from collections import deque
from keepalive import keepalive # to keep bot running 24/7 and prevent shutdown
keepalive()

dbDIR = os.path.dirname(os.path.abspath(__file__))   # set to storee db in this directory
GUILD = 12345678910
song_queues = {}

load_dotenv()
token = os.getenv("TOKEN")   # token is stored in this variable

async def search_ytdlp_async(query, ydl_opts): #handling current execution of song
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: extract(query, ydl_opts))

def extract(query, ydl_opts):   #searching for a song
    with ydl_opts.YoutubeDL(ydl_opts) as ydl: 
        return ydl.extract_info(query, download = False)

intents = discord.Intents.default()
intents.message_content = True   # bot permission to message

bot = commands.Bot (command_prefix = "!", intents = intents )


@bot.event
async def on_ready(): # remove _temp
    guildrun = discord.Object(id=GUILD)
    await bot.tree.sync(guild = guildrun) # enable /commands
    print(f"{bot.user} is online and ready to play!")  #just give a heads up when online
    
    
@bot.tree.command(name="play", description="play a song or add in queue")
@app_commands.describe(song_query = "Search query")
async def play(interaction: discord.Interaction, song_query: str):
    await interaction.response.defer() # might take 3sec or longer for response
    
    member = interaction.user if isinstance(interaction.user, discord.Member) else None
    VC = member.voice if member else None
    
    if VC is None or VC.channel is None: # not in a VC
        await interaction.followup.send("Not in a VC bruh")
        return
    
    if interaction.guild is None:
        await interaction.followup.send("This command can only be used in a server.")
        return

    VCclient = interaction.guild.voice_client
    if VCclient is None:
        VCclient = await VC.channel.connect()
    elif VC.channel != VCclient.channel:
        if isinstance(VCclient, discord.VoiceClient):
            await VCclient.move_to(VC.channel)
        else:
            await interaction.followup.send("Unable to move to the requested voice channel.")
            return
    ydl_options = {
        "format": "bestaudio[abr<=96]/bestaudio",
        "noplaylist": True,
        "youtube_include_dash_manifest": False,
        "youtube_include_hls_manifest": False,
    } # check the ydl documentation for options
    
    query = "ytsearch1: " + song_query # ytsearch1 will search the top first result from search
    
    
    
    search_result = await search_ytdlp_async(query, ydl_options)
    tracks = search_result.get("entries",[])
    
    if tracks is None:
        await interaction.followup.send("No resluts found")
        return
    
    soundtrack = tracks[0]
    url = soundtrack["url"]
    title = soundtrack.get("title", "Untitled")
    
    guild_id = str(interaction.guild_id)
    if song_queues.get(guild_id) is None:
        song_queues[guild_id] = deque()
        
    song_queues[guild_id].append((url, title)) # add data to dictionary
    
    if isinstance(VCclient, discord.VoiceClient) and (VCclient.is_playing() or VCclient.is_paused()):
        await interaction.followup.send(f"{title} has been added to the playlist")
    else:
        await interaction.followup.send(f"{title} is now playing")
        await play_next_song(voice_client=VCclient, guild_id=guild_id, channel=interaction.channel)
        
#skip command
@bot.tree.command(name="skip", description="Skip the current song from the playlist")
async def skip(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client if interaction.guild is not None else None
    if isinstance(voice_client, discord.VoiceClient) and (voice_client.is_playing() or voice_client.is_paused()):
        voice_client.stop()
        await interaction.response.send_message(f"Skipped current song")
    else:
        await interaction.response.send_message("Empty playlist")
        
#pause command
@bot.tree.command(name="pause", description="Pause the current song")
async def pause(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client if interaction.guild is not None else None

    #check if bot is in call
    if not isinstance(voice_client, discord.VoiceClient):
        return await interaction.response.send_message("No contact with the radio call")
    #check if something is playing
    if not voice_client or not voice_client.is_playing():
        return await interaction.response.send_message("No music to my ears")
    #pause the track
    voice_client.pause()

#resume command
@bot.tree.command(name="resume", description="Resume the current song")
async def resume(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client if interaction.guild is not None else None

    #check if bot is in call
    if not isinstance(voice_client, discord.VoiceClient):
        return await interaction.response.send_message("No contact with the radio call")
    #check if something is playing
    if not voice_client or not voice_client.is_playing():
        return await interaction.response.send_message("No music to my ears")
    #resume the track
    voice_client.resume()
    
    
#stop command
@bot.tree.command(name="stop", description="Stops playing music")
async def stop(interaction: discord.Interaction):
    await interaction.response.defer()
    voice_client = interaction.guild.voice_client if interaction.guild is not None else None
    
    #check if bot is in a VC
    if not isinstance(voice_client, discord.VoiceClient) or not voice_client.is_connected():
        await interaction.followup.send("Out of range to the call channel")
        return
    #clear guild request for song
    guildidstr = str(interaction.guild_id)
    if guildidstr in song_queues:
        song_queues[guildidstr].clear()
    #stop all play or pause activity
    if isinstance(voice_client, discord.VoiceClient) and (voice_client.is_playing() or voice_client.is_paused()):
        voice_client.stop()
        
    await interaction.response.send_message("song session ended ")
    
    #disconnect from channel(optional)
    await voice_client.disconnect()
    
    
    

    

    
async def play_next_song(voice_client, guild_id, channel):
    if song_queues[guild_id]:
        url, title = song_queues[guild_id].popleft()
        
        ffmpeg_executable = "bin\\ffmpeg\\ffmpeg.exe"
        before_options = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5" #audio connectivity
        options = "-vn -c:a libopus -b:a 96k" #remove video part, opus encoded, 96kb bitrate
        bin = discord.FFmpegOpusAudio(url, executable=ffmpeg_executable, before_options=before_options, options=options)
        
        def after_play(error):
            if error:
                print(f"Error playing {title}")
            asyncio.run_coroutine_threadsafe(play_next_song(voice_client=voice_client, guild_id=GUILD, channel=channel), bot.loop)
        
        if isinstance(voice_client, discord.VoiceClient):
            voice_client.play(bin, after=after_play)
        asyncio.create_task(channel.send(f"Now Playing: {title}"))
        
    else:
        
        await voice_client.disconnect()
        song_queues[guild_id] = deque()
        
        
    
bot.run("")