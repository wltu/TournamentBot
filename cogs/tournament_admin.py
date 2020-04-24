import discord
from discord.ext import commands

class TournamentAdmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def setup(self, context):
        '''
            Setup tournament.
            Supported format includes:
            - single elimination -> se
            - double elimination -> de
            - round robin -> rr

            Type !setup help format for more info on a the selected format.
        '''
        await context.send("Test setup")
