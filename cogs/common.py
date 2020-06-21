import discord
import os
import youtube_dl
from discord.utils import get
from discord.ext import commands


class Common(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def play_audio(self, file, voice):
        if os.name != 'nt' and not discord.opus.is_loaded():
            try:
                # full extension for alpine docker image
                discord.opus.load_opus('libopus.so.0')
            except OSError:
                discord.opus.load_opus('opus')

        audio_source = discord.FFmpegPCMAudio(file)
        voice.play(audio_source)

    @commands.command(name="test")
    async def test(self, ctx, arg):
        """ Test Command """
        await ctx.send(arg)

    @commands.command(name="play")
    async def play(self, ctx, url):
        """ Play Music from YouTube """
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if not voice or not voice.is_connected():
            await self.join(ctx)
            voice = get(self.bot.voice_clients, guild=ctx.guild)

            if not voice:
                return

        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio!")
            ydl.download([url])

        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                print("Downloaded {file}")
                try:
                    os.rename(file, "current.mp3")
                except WindowsError:
                    os.remove("current.mp3")
                    os.rename(file, "current.mp3")
        # discord.opus.load_opus()
        self.play_audio("current.mp3", voice)

    @commands.command(name="join")
    async def join(self, ctx):
        """ Join Your Current Voice Channel """
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

                self.play_audio("sound/aqua_cry.mp3", voice)
        else:
            voice = await channel.connect()
            self.play_audio("sound/aqua_cry.mp3", voice)

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
        """ Leave Current Voice Channel """
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice is not None:
            await voice.disconnect()
        else:
            await ctx.send("I am currently not in a voice chat! :cry:")
