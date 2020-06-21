import discord
from discord.utils import get
from discord.ext import commands
from rulesets.single_elimination import SingleElimination


class TournamentOrganizer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_tournament = None
        self.channels = []
        self.channel_map = {}
        self.main_channel = None
        self.current_category = None
        self.current_TO = None

    async def clean_tournament_channels(self):
        """ Remove tournament channels """
        for channel in self.channels:
            await channel.delete()

        self.channels = []
        self.channel_map = {}

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if self.main_channel == None:
            return

        channel = after.channel

        if channel == self.main_channel:
            channel_id = self.channel_map.get(member.display_name, -1)

            if channel_id == -1:
                await member.move_to(None)
            else:
                await member.move_to(self.channels[channel_id])

    @commands.command(name="clean")
    async def clean(self, ctx):
        """
            Remove all the tournament voice channels.
        """
        await self.clean_tournament_channels()

    @commands.group(name="setup")
    async def setup(self, ctx):
        """
            Setup tournament.
            Supported format includes:
            - single elimination -> se
            - double elimination -> de
            - round robin -> rr

            Type !help setup [format] for more info on a the selected format.
        """
        self.current_TO = ctx.author

        guild = ctx.guild

        tournament_category = get(guild.categories, name="Tournament Matches")
        if not tournament_category:
            tournament_category = await guild.create_category("Tournament Matches")

        overwrites = tournament_category.overwrites_for(ctx.guild.default_role)
        overwrites.connect = True
        overwrites.move_members = False
        overwrites.view_channel = False

        try:
            await tournament_category.set_permissions(
                ctx.guild.default_role, overwrite=overwrites
            )
        except discord.Forbidden:
            print("Cannot update permission for category!")

        main_channel = get(guild.channels, name="Tournament Lobby")

        if not main_channel:
            main_channel = await guild.create_voice_channel(
                "Tournament Lobby", sync_permissions=False
            )

        overwrites = main_channel.overwrites_for(ctx.guild.default_role)
        overwrites.connect = True
        overwrites.move_members = False
        overwrites.view_channel = True
        overwrites.speak = False

        try:
            await main_channel.set_permissions(
                ctx.guild.default_role, overwrite=overwrites
            )
        except discord.Forbidden:
            print("Cannot update permission for channel!")

        bot_role = get(guild.roles, name="TournamentBot")

        overwrites = main_channel.overwrites_for(bot_role)
        overwrites.move_members = True

        try:
            await main_channel.set_permissions(bot_role, overwrite=overwrites)
        except discord.Forbidden:
            print("Cannot update permission for channel!")

        self.current_category = tournament_category
        self.main_channel = main_channel

        await ctx.send("Setuping up tournament...")

    @commands.command(name="signup")
    async def signup(self, ctx, member: discord.Member = None):
        """
            Signup for current tournament.
        """

        if not self.current_tournament:
            await ctx.send("No tournament currently available! Start one with `!setup [format]")
            return

        if ctx.author != self.current_TO or member == None:
            member = ctx.author

        if self.current_tournament.add_player(member):
            await ctx.send(member.display_name + " is now signed up!")
        else:
            await ctx.send(member.display_name + " is already signed up!")

    @commands.command(name="report")
    async def report(self, ctx, result: int, match_id: int = -1):
        """
            Report result for current tournament.
        """

        if not self.current_tournament:
            await ctx.send(
                "No tournament currently going on... start one with `!setup [format]`."
            )
            return

        if ctx.author == self.current_TO:
            self.current_tournament.update_match(match_id, result)
        else:
            player = self.current_tournament.player_map[ctx.display_name]
            self.current_tournament.update_match(player.current_match, result)

    @report.error
    async def report_error(self, ctx, error): 
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
            "Missing Arguments. Try `!help report`.\n" + 
            "Example: `!report 1 13`\n" +
            "Player 1 won in match 13."
            )
            return
        
        raise error

    @commands.command(name="start")
    async def start(self, ctx):
        """
            Start current tournament!
        """

        if not self.current_TO:
            await ctx.send("There is currently no tournament. Try `!setup [format]`")
            return

        if ctx.author != self.current_TO:
            await ctx.send("Only the current TO can starte the tournament!")
            return

        bracket = self.current_tournament.start_tournament()

        await ctx.send("Tournament Started!")
        await ctx.send("```" + bracket + "```")

        guild = ctx.guild

        invite = await self.main_channel.create_invite()

        i = 0
        for match_id in self.current_tournament.valid_matches:
            match = self.current_tournament.valid_matches[match_id]

            channel = await guild.create_voice_channel(
                "match" + str(i), category=self.current_category, sync_permissions=True
            )
            self.channels.append(channel)

            for player in [match.player_one, match.player_two]:
                self.channel_map[player.name] = i

                dm = player.user.dm_channel
                if not dm:
                    dm = await player.user.create_dm()

                await dm.send(invite)

            i += 1

    @setup.command(name="single_elimination", aliases=["se"])
    async def single_elimination(self, ctx):
        """
            Single Elimination Bracket
        """
        self.current_tournament = SingleElimination()

        await ctx.send("Single Elimination Bracket setted up. Signup!")

    @setup.command(name="double_elimination", aliases=["de"])
    async def double_elimination(self, ctx):
        """
            Double Elimination
        """
        await ctx.send("double Elimination")

    @setup.command(name="round_robin", aliases=["rr"])
    async def round_robin(self, ctx):
        """
            Round Robin
        """
        await ctx.send("Round Robin")
