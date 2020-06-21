import asyncio
import discord
import os
import youtube_dl
from discord.utils import get
from discord.ext import commands


class Common(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.playing_music = {}

    def user_channel(self, ctx):
        if ctx.message.author.voice is None:
            return None, False

        return ctx.message.author.voice.channel, True

    def clean_songs(self, guild_id):
        dir = "./play/" + str(guild_id)
        filelist = [f for f in os.listdir(dir) if f.endswith(".mp3")]
        for f in filelist:
            os.remove(os.path.join(dir, f))

    async def join_channel(self, ctx, channel=None):
        if not ctx.message.author.voice:
            await ctx.send("You are not in a channel :angry:")
            return None

        if not channel:
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
        else:
            voice = await channel.connect()

        return voice

    def play_audio(self, voice, song):
        if os.name != "nt" and not discord.opus.is_loaded():
            try:
                # full extension for alpine docker image
                discord.opus.load_opus("libopus.so.0")
            except OSError:
                discord.opus.load_opus("opus")

        if voice.is_playing():
            voice.stop()
        audio_source = discord.FFmpegPCMAudio(song)
        voice.play(audio_source)

    @commands.command(name="test")
    async def test(self, ctx, arg):
        """ Test Command """
        await ctx.send(arg)

    @commands.command(name="play")
    async def play(self, ctx, url):
        """ Play Music from YouTube """
        if not ctx.message.author.voice:
            await ctx.send("You are not in a channel :angry:")
            return

        channel = ctx.message.author.voice.channel

        voice = get(self.bot.voice_clients, guild=ctx.guild)
        guild_id = str(ctx.guild.id)
        ydl_opts = {
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
            "outtmpl": "./play/" + guild_id + "/%(title)s.%(ext)s",
            "forcefilename": True,
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            if not voice or not voice.is_playing():
                print("Downloading audio!")

                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                filename = filename[:-5]

                if not voice or not voice.is_connected():
                    if not voice:
                        voice = await channel.connect()
                    else:
                        await voice.move_to(channel)
                
                await ctx.send(
                    "Playing `" + filename[8 + len(guild_id):] + "` in `" + str(channel) + "`"
                )
                self.playing_music[ctx.guild.id] = True 
                self.play_audio(voice, filename + ".mp3")
            else:
                await ctx.send("Music is being played in " + str(voice.channel) + "!")

    @commands.command(name="join")
    async def join(self, ctx):
        """ Join Your Current Voice Channel """

        voice = await self.join_channel(ctx)

        if voice:
            self.play_audio(voice=voice, song="sound/aqua_cry.mp3")

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
            self.playing_music[ctx.guild.id] = False
            self.clean_songs(ctx.guild.id)
            await voice.disconnect()
        else:
            await ctx.send("I am currently not in a voice chat! :cry:")
