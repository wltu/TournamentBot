import discord
import os
import youtube_dl
from discord.utils import get
from discord.ext import commands


class Common(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_song = None
        self.song_queue = []
        self.voice_channel = None

    def after_audio(self, error):
        self.song_queue = self.song_queue[1:]

        if len(self.song_queue) > 0:
            print("Play next song!")
            self.play_audio(self.voice_channel)
        else:
            dir = './play'
            filelist = [ f for f in os.listdir(dir) if f.endswith(".mp3") ]
            for f in filelist:
                os.remove(os.path.join(dir, f))

    def play_audio(self, voice, song=None):
        if os.name != "nt" and not discord.opus.is_loaded():
            try:
                # full extension for alpine docker image
                discord.opus.load_opus("libopus.so.0")
            except OSError:
                discord.opus.load_opus("opus")

        if voice.is_playing():
            voice.stop()

        self.voice_channel = voice

        if not song:
            audio_source = discord.FFmpegPCMAudio(self.song_queue[0])
            voice.play(audio_source, after=self.after_audio)
        else:
            audio_source = discord.FFmpegPCMAudio(song)
            voice.play(audio_source, after=None)

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
            "outtmpl": "./play/%(title)s.%(ext)s",
            "forcefilename": True,
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            filename = ydl.prepare_filename(info)
            filename = filename[:-5]

            if filename + ".mp3" not in self.song_queue:
                print("Downloading audio!")
                ydl.download([url])
            
            self.song_queue.append(filename + ".mp3")
            if not voice.is_playing():
                await ctx.send("Playing `" + filename[5:] + "` in " + str(voice.channel))
                self.play_audio(voice)
            else:
                await ctx.send("Putting `" + filename[5:] + "` in the queue.")

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

                self.play_audio(voice=voice, song="sound/aqua_cry.mp3")

        else:
            voice = await channel.connect()
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
            await voice.disconnect()
        else:
            await ctx.send("I am currently not in a voice chat! :cry:")
