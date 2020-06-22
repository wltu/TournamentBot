import discord
import argparse

from discord.ext import commands
from discord.utils import get

# from rulesets import double_elimination
from rulesets import single_elimination
from rulesets import match
from cogs.tournament_organizer import TournamentOrganizer
from cogs.common import Common


def main():
    parser = argparse.ArgumentParser(description="Starting TournamentBot.")
    parser.add_argument("token", type=str, help="discord bot token")

    args = parser.parse_args()

    # client = discord.Client()
    client = commands.Bot(
        command_prefix="!", description="TournamentBot for your tournaments"
    )

    @client.event
    async def on_ready():
        print("We have logged in as {0.user}".format(client))

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith("$hello"):
            await message.channel.send("Hello!")

        await client.process_commands(message)

    @client.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.channel.send(
                "Invalid commmands. Try `!help` to get more information!"
            )

        if not isinstance(error, commands.MissingRequiredArgument):
            raise error

    client.help_command.cog = Common(client)
    client.add_cog(TournamentOrganizer(client))
    client.add_cog(client.help_command.cog)

    client.run(args.token)


def test_rulesets():
    # de = double_elimination.DoubleElimination()
    # de.add_player("yes")
    # de.add_player("no")
    # de.add_player("ok")
    # de.add_player("nol")

    # print(de.get_players())
    # print(de.get_initial_bracket())
    # m0 = match.Match("abc", "abcd", 10)

    # m1 = match.LeafBracketMatch("abc", m0, 10)
    # x = m1.draw_bracket(1)
    # for y in x:
    #     print(y)
    # m = match.Match("abc", "abcd", 10)
    # x = m.draw_bracket(1)
    # print('                 |--')

    # for y in x:
    #     print(3 * ' ' + y)
    from test.mock.mock_member import MockMember

    se = single_elimination.SingleElimination()
    se.add_player(MockMember("0"))
    se.add_player(MockMember("1"))
    se.add_player(MockMember("2"))
    se.add_player(MockMember("3"))
    # se.add_player(MockMember("4"))
    # se.add_player(MockMember("5"))
    # se.add_player(MockMember("6"))
    # se.add_player(MockMember("7"))
    # se.add_player(MockMember("8"))
    # se.add_player(MockMember("9"))
    # se.add_player(MockMember("10"))
    # se.add_player(MockMember("11"))
    # se.add_player(MockMember("12"))
    # se.add_player(MockMember("13"))
    # se.add_player(MockMember("14"))
    # se.add_player(MockMember("15"))
    bracket, _ = se.start_tournament(False)
    print(bracket)

    # for key, val in se.valid_matches.items():
    #     print(key)
    #     print(val.summary())
    
    # se.update_match(7, 0)

    # print("update")

    # for key, val in se.valid_matches.items():
    #     print(key)
    #     print(val.summary())


    # print(se.get_initial_bracket())

    # tournament.player_map["player0"].next_match()

    print(se.player_map["0"].current_match.summary())
    print(se.player_map["0"].get_opponent())
    print(se.player_map["2"].name)
    print(se.player_map["2"].current_match.summary())
    print(se.player_map["2"].get_opponent())

    se.update_match(1, 0)
    print(se.player_map["0"].current_match.summary())
    print(se.player_map["0"].get_opponent())

    


if __name__ == "__main__":
    main()
    # test_rulesets()
