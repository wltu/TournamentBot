import discord
from discord.ext import commands
from rulesets.single_elimination import SingleElimination


class TournamentOrganizer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_tournament = None
        self.channels = []
        self.current_category = None
        self.current_TO = None

    async def clean_tournament_channels(self):
        ''' Remove tournament channels '''
        for channel in self.channels:
            await channel.delete()

        self.channels = []

    @commands.group(name='setup')
    async def setup(self, ctx):
        '''
            Setup tournament.
            Supported format includes:
            - single elimination -> se
            - double elimination -> de
            - round robin -> rr

            Type !setup help format for more info on a the selected format.
        '''
        self.current_TO = ctx.author

        guild = ctx.guild
        categories = guild.categories

        tournament_category = None
        for category in categories:
            if category.name == 'Tournament Matches':
                tournament_category = category

        if not tournament_category:
            tournament_category = await guild.create_category('Tournament Matches')

        self.current_category = tournament_category

        overwrites = tournament_category.overwrites_for(ctx.guild.default_role)
        overwrites.connect = False
        overwrites.move_members = False
        overwrites.view_channel = True

        try:
            await tournament_category.set_permissions(ctx.guild.default_role, overwrite=overwrites)
        except discord.Forbidden:
            print("Cannot update permission!")

        await ctx.send("Setuping up tournament...")

    @commands.command(name="signup")
    async def signup(self, ctx, member: discord.Member = None):
        '''
            Signup for current tournament.
        '''
        if ctx.author != self.current_TO or member == None:
            member = ctx.author

        if self.current_tournament.add_player(member):
            await ctx.send(member.display_name + " is now signed up!")
        else:
            await ctx.send(member.display_name + " is already signed up!")

    @commands.command(name="report")
    async def report(self, ctx, result: int, match_id: int = -1):
        '''
            Report result for current tournament.
        '''

        if self.current_tournament == None:
            await ctx.send("No tournament currently going on... start one with `!setup`.")

        if ctx.author == self.current_TO:
            self.current_tournament.update_match(match_id, result)
        else:
            player = self.current_tournament.player_map[ctx.display_name]
            self.current_tournament.update_match(player.current_match, result)

    @commands.command(name="start")
    async def start(self, ctx):
        '''
            Start current tournament!
        '''
        if ctx.author != self.current_TO:
            await ctx.send("Only the TO can starte the tournament!")

        bracket = self.current_tournament.start_tournament()

        await ctx.send("Tournament Started!")
        await ctx.send('```' + bracket + '```')

        guild = ctx.guild
        i = 0
        for match_id in self.current_tournament.valid_matches:
            match = self.current_tournament.valid_matches[match_id]

            channel = await guild.create_voice_channel('match' + str(i),
                                                       category=self.current_category,
                                                       sync_permissions=True)
            self.channels.append(channel)
            invite = await channel.create_invite(max_uses=2)
    
            for player in [match.player_one, match.player_two]: 
                dm = player.user.dm_channel
                if not dm:
                    dm = await player.user.create_dm()
                
                await dm.send(invite)

    @setup.command(name="single_elimination", aliases=['se'])
    async def single_elimination(self, ctx):
        '''
            Single Elimination
        '''
        self.current_tournament = SingleElimination()

        await ctx.send("Single Elimination setted up. Signup")

    @setup.command(name="double_elimination", aliases=['de'])
    async def double_elimination(self, ctx):
        '''
            Double Elimination
        '''
        await ctx.send("double Elimination")

    @setup.command(name="round_robin", aliases=['rr'])
    async def round_robin(self, ctx):
        '''
            Round Robin
        '''
        await ctx.send("Round Robin")
