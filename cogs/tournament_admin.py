import discord
from discord.ext import commands

class TournamentAdmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name = 'setup')
    async def setup(self, context):
        '''
            Setup tournament.
            Supported format includes:
            - single elimination -> se
            - double elimination -> de
            - round robin -> rr

            Type !setup help format for more info on a the selected format.
        '''
        await context.send("Setuping up tournament...")


    @setup.command(name ="single_elimination", aliases=['se'])
    async def single_elimination(self, context):
        '''
            Single Elimination
        '''
        await context.send("Single Elimination")

    @setup.command(name ="double_elimination", aliases=['de'])
    async def double_elimination(self, context):
        '''
            Double Elimination
        '''
        await context.send("double Elimination")

    @setup.command(name ="round_robin", aliases=['rr'])
    async def round_robin(self, context):
        '''
            Round Robin
        '''
        await context.send("Round Robin")
