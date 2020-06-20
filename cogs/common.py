import discord
import os
import youtube_dl
from discord.utils import get
from discord.ext import commands


class Common(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="test")
    async def test(self, ctx, arg):
        """ Test Command """
        await ctx.send(arg)

    @commands.command(name="play")
    async def play(self, ctx, url):
        """ Play Music """
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    'preferredquality': '192',
                }
            ],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio!")
            ydl.download([url])

        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                print("Downloaded {file}")
                os.rename(file, "current.mp3")
        
        audio_source = discord.FFmpegPCMAudio("current.mp3")
        voice.play(audio_source)

    @commands.command(name="join")
    async def join(self, ctx):
        """ Join Voice Channel Command """
        if ctx.message.author.voice is None:
            await ctx.send("You are not in a channel :angry:")
            return

        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():

            if voice.channel == channel:
                await ctx.send("I am already in " + str(channel) + "!")
            else:
                await ctx.send(
                    "I am moving from " + str(voice.channel) + " to " + str(channel) 
                )
                await voice.move_to(channel)
                audio_source = discord.FFmpegPCMAudio("sound/aqua_cry.mp3")
                voice.play(audio_source)
        else:
            voice = await channel.connect()
            audio_source = discord.FFmpegPCMAudio("sound/aqua_cry.mp3")
            voice.play(audio_source)

    @commands.command(name="chat")
    async def chat(self, ctx, user: discord.User):
        """ Chat another member Command """

        # await member.user.create_dm()
        dm = user.dm_channel

        if not dm:
            dm = await user.create_dm()

        await dm.send("Hello")

    @commands.command(name="leave")
    async def leave(self, ctx):
        """ Leave Voice Channel Command """
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice is not None:
            await voice.disconnect()
        else:
            await ctx.send("I am currently not in a voice chat! :cry:")

