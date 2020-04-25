import discord
from discord.ext import commands
from rulesets.single_elimination import SingleElimination 


class TournamentOrganizer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_tournament = None

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

    @commands.command(name ="signup")
    async def signup(self, context, name : str):
        '''
            Signup for current tournament.
        '''
        self.current_tournament.add_player(name)

        await context.send(name + " is now signed up!")

    @commands.command(name ="start")
    async def start(self, context):
        '''
            Start current tournament!
        '''
        
        bracket = self.current_tournament.start_tournament()

        await context.send("Tournament Started!")
        await context.send('```' + bracket + '```')

    @setup.command(name ="single_elimination", aliases=['se'])
    async def single_elimination(self, context):
        '''
            Single Elimination
        '''
        self.current_tournament = SingleElimination()

        await context.send("Single Elimination setted up. Signup")

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
