import asyncio
import discord
from discord.utils import get
from discord.ext import commands
from rulesets.single_elimination import SingleElimination


class Tournament:
    def __init__(self):
        self.current_tournament = None
        self.channels = []
        self.channel_map = {}
        self.main_channel = None
        self.current_category = None
        self.current_TO = None
        self.last_tournament = None
        self.valid = False
        self.invite = None


class TournamentOrganizer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tournament_map = {}

        self.current_tournament = None
        self.channels = []
        self.channel_map = {}
        self.main_channel = None
        self.current_category = None
        self.current_TO = None
        self.last_tournament = None
        self.valid = False

        self.no_tournament_message = (
            "No tournament currently available! Start one with `!setup [format]`"
        )

    async def after_update_match(self, ctx, winner, player):
        """ Action after updating a match result """
        current_server = self.tournament_map[ctx.guild.id]

        if winner:
            await ctx.send(winner.mention + " won the tournament! Nice.")

            await ctx.send("Final Tournament Ranking!")
            await ctx.send(current_server.current_tournament.get_ranking())

            await self.end(ctx)
        else:
            match = player.current_match
            if match.check_match:
                match_vc_id = current_server.channel_map[player.id]

                for player in [match.player_one, match.player_two]:
                    current_server.channel_map[player.id] = match_vc_id

                    dm = player.user.dm_channel
                    if not dm:
                        dm = await player.user.create_dm()
                    await dm.send(
                        "{} vs. {}\n{}".format(
                            match.player_one.name,
                            match.player_two.name,
                            current_server.invite,
                        )
                    )

    async def clean_tournament_channels(self, ctx):
        """ Remove tournament channels """
        current_server = self.tournament_map[ctx.guild.id]

        for channel in current_server.channels:
            await channel.delete()

        current_server.channels = []
        current_server.channel_map = {}

    @commands.Cog.listener()
    async def on_guild_available(self, guild):
        self.tournament_map[guild.id] = Tournament()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        current_server = self.tournament_map[member.guild.id]

        if current_server.main_channel == None:
            return

        channel = after.channel

        if channel == current_server.main_channel:
            channel_id = current_server.channel_map.get(member.id, -1)

            if channel_id == -1:
                await member.move_to(None)
            else:
                await member.move_to(current_server.channels[channel_id])

    @commands.command(name="end")
    async def end(self, ctx):
        """
            End the current tournament and remove all the tournament voice channels.
        """
        current_server = self.tournament_map[ctx.guild.id]

        current_server.last_tournament = current_server.current_tournament
        current_server.current_tournament = None
        current_server.current_TO = None
        current_server.current_category = None
        current_server.valid = False
        current_server.invite = None

        await self.clean_tournament_channels(ctx)

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
        self.tournament_map[ctx.guild.id].current_TO = ctx.author

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

        self.tournament_map[ctx.guild.id].current_category = tournament_category
        self.tournament_map[ctx.guild.id].main_channel = main_channel

        await ctx.send("Setuping up tournament...")

    @commands.command(name="signup")
    async def signup(self, ctx, member: discord.Member = None):
        """
            Signup for current tournament.
        """
        current_server = self.tournament_map[ctx.guild.id]

        if not current_server.current_tournament:
            await ctx.send(self.no_tournament_message)
            return

        if current_server.valid:
            await ctx.send("Current tournament already started!")
            return

        if ctx.author != current_server.current_TO or member == None:
            member = ctx.author

        if current_server.current_tournament.add_player(member):
            await ctx.send(member.mention + " is now signed up!")
        else:
            await ctx.send(member.mention + " is already signed up!")

    @commands.command(name="update")
    async def update(self, ctx, match_id: int, member: discord.Member):
        """
            Update match resutre for current tournament.
            Tournament Organizer only.
        """
        current_server = self.tournament_map[ctx.guild.id]

        if not current_server.current_tournament:
            await ctx.send(self.no_tournament_message)
            return

        if not current_server.valid:
            await ctx.send("Current tournament has not started!")
            return

        winner = None

        if ctx.author == current_server.current_TO:
            player = current_server.current_tournament.player_map.get(
                ctx.author.id, None
            )
            match = player.current_match

            if not player:
                await ctx.send(ctx.author + " is not in the tournament!")
                return

            try:
                winner = current_server.current_tournament.update_match(
                    match_id, member.id
                )
                if match.player_one.id == member.id:
                    del current_server.channel_map[match.player_two.id]
                else:
                    del current_server.channel_map[match.player_one.id]
            except ValueError:
                await ctx.send(member.mention + " is not in the match!")
                return

            await self.after_update_match(ctx, winner, player)
        else:
            await ctx.send("Only the current tournament's TO can use this command!")
            return

    @commands.command(name="report")
    async def report(self, ctx, member: discord.Member):
        """
            Report your match result for current tournament.
        """
        current_server = self.tournament_map[ctx.guild.id]
        if not current_server.current_tournament:
            await ctx.send(self.no_tournament_message)
            return

        if not current_server.valid:
            await ctx.send("Current tournament has not started!")
            return

        player = current_server.current_tournament.player_map.get(ctx.author.id, None)

        if not player:
            await ctx.send(ctx.author + " is not in the tournament!")
            return

        match = player.current_match
        players = [match.player_one.id, match.player_two.id]

        if member.id not in players:
            await ctx.send(member.mention + " is not in the match!")
            return

        channel = current_server.channels[current_server.channel_map[player.id]]
        player_one = member

        player_id = players[0]
        if players[0] == member.id:
            player_id = players[1]

        player_two = await ctx.guild.fetch_member(player_id)

        if (
            not player_one.voice
            or player_one.voice.channel != channel
            or not player_two.voice
            or player_two.voice.channel != channel
        ):
            await ctx.send(
                "Both members of the match must be in the match voice chat to report result!"
            )
            return

        report_megssage = match.summary() + " -> " + member.mention + " won? "
        message = await ctx.send(
            report_megssage + player_two.mention + " please confrim!"
        )
        await message.add_reaction("☑️")
        await message.add_reaction("❌")

        def check(reaction, user):
            return (
                user == player_two
                and reaction.message.id == message.id
                and (reaction.emoji == "☑️" or reaction.emoji == "❌")
            )

        try:
            reaction, _ = await self.bot.wait_for(
                "reaction_add", timeout=30.0, check=check
            )

            if reaction.emoji == "☑️":
                winner = current_server.current_tournament.update_match(
                    match.match_id, member.id
                )

                del current_server.channel_map[player_two.id]

                await message.edit(
                    content=report_megssage + " Confirmed!", suppress=True
                )

                await self.after_update_match(ctx, winner, player)
            else:
                await message.edit(
                    content=report_megssage + " Report canceled!", suppress=True
                )
        except asyncio.TimeoutError:
            await message.edit(
                content=report_megssage + " Report canceled!", suppress=True
            )

    @report.error
    async def report_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                "Missing Arguments. Try `!help report`.\n"
                + "Example: `!report 1 13`\n"
                + "Player 1 won in match 13."
            )
            return

        raise error

    @commands.command(name="start")
    async def start(self, ctx, shuffle=True):
        """
            Start current tournament!
        """
        current_server = self.tournament_map[ctx.guild.id]

        if not current_server.current_TO:
            await ctx.send("There is currently no tournament. Try `!setup [format]`")
            return

        if ctx.author != current_server.current_TO:
            await ctx.send("Only the current TO can start the tournament!")
            return

        bracket, valid = current_server.current_tournament.start_tournament(shuffle)

        if not valid:
            await ctx.send(
                "Not enough players to start the tournament! Must have at least 2 players."
            )
            return
        current_server.valid = True
        await ctx.send("Tournament Started!")
        await ctx.send("```" + bracket + "```")

        guild = ctx.guild
        current_server.invite = await current_server.main_channel.create_invite()

        i = 0
        for match_id in current_server.current_tournament.valid_matches:
            match = current_server.current_tournament.valid_matches[match_id]

            if match.check_match():
                channel = await guild.create_voice_channel(
                    "match" + str(i),
                    category=current_server.current_category,
                    sync_permissions=True,
                )
                current_server.channels.append(channel)

                for player in [match.player_one, match.player_two]:
                    current_server.channel_map[player.id] = i

                    dm = player.user.dm_channel
                    if not dm:
                        dm = await player.user.create_dm()

                    await dm.send(
                        "{} vs. {}\n{}".format(
                            match.player_one.name,
                            match.player_two.name,
                            current_server.invite,
                        )
                    )

                i += 1

    @commands.command(name="matches")
    async def matches(self, ctx, detail=False):
        """
            Show all ongoing matches in current tournament
            Set detail to true to show match id.
        """

        current_server = self.tournament_map[ctx.guild.id]

        if not current_server.current_tournament:
            await ctx.send(self.no_tournament_message)
            return

        if not current_server.valid:
            await ctx.send("Current tournament has not started!")
            return

        matches = current_server.current_tournament.valid_matches
        output = ""

        for _, match in matches.items():
            if detail:
                output += match.detailed_summary() + "\n"
            else:
                output += match.summary() + "\n"

        await ctx.send("All ongoing matches for the current tournament!")
        await ctx.send(output)

    @commands.command(name="opponent")
    async def opponent(self, ctx):
        """
            Show the opponents for your next match. 
        """
        player_id = ctx.author.id

        if not current_server.current_tournament:
            await ctx.send(self.no_tournament_message)
            return

        await ctx.send(current_server.current_tournament.get_opponent(player_id))

    @commands.command(name="rank")
    async def rank(self, ctx):
        """
            Show your tournament rank along with overall ranks in the current tournament.
            If no tournament active, show the most recent tournament
        """
        player_id = ctx.author.id

        current_server = self.tournament_map[ctx.guild.id]
        if current_server.current_tournament:
            await ctx.send("Current tournament ranking!")
            await ctx.send(current_server.current_tournament.get_ranking(player_id))

            ranking = current_server.current_tournament.get_ranking()
            if len(ranking) == 0:
                await ctx.send("Tournament just started... No one is out yet!")
            else:
                await ctx.send(ranking)

        elif current_server.last_tournament:
            await ctx.send("Ranking for the last tournament!")
            await ctx.send(current_server.last_tournament.get_ranking(player_id))

            ranking = current_server.last_tournament.get_ranking()

            if len(ranking) == 0:
                await ctx.send(
                    "Thank's weird?? The tournament did not finish properly!"
                )
            else:
                await ctx.send(ranking)
        else:
            await ctx.send("No past tournament within this server!")

    @commands.command(name="history")
    async def history(self, ctx):
        """
            Show your match history for current tournament.
            If no tournament active, show the most recent tournament
        """
        player_id = ctx.author.id

        current_server = self.tournament_map[ctx.guild.id]

        if current_server.current_tournament:
            await ctx.send("Your match history from the current tournament")
            await ctx.send(current_server.current_tournament.get_history(player_id))
        elif current_server.last_tournament:
            await ctx.send("Your match history from the last tournament")
            await ctx.send(current_server.last_tournament.get_history(player_id))
        else:
            await ctx.send("No past tournament within this server!")

    @setup.command(name="single_elimination", aliases=["se"])
    async def single_elimination(self, ctx):
        """
            Single Elimination Bracket
        """
        self.tournament_map[ctx.guild.id].current_tournament = SingleElimination()

        await ctx.send("Single Elimination Bracket setted up. Signup!")

    @setup.command(name="double_elimination", aliases=["de"])
    async def double_elimination(self, ctx):
        """
            Double Elimination Bracket
        """
        await ctx.send("TODO: Double Elimination")

    @setup.command(name="round_robin", aliases=["rr"])
    async def round_robin(self, ctx):
        """
            Round Robin
        """
        await ctx.send("TODO: Round Robin")
    
    @setup.command(name="ladder", aliases=["l"])
    async def ladder(self, ctx):
        """
            Ladder
        """
        await ctx.send("TODO: Ladder")
