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

    se = single_elimination.SingleElimination()
    se.add_player("0")
    se.add_player("1")
    se.add_player("2")
    se.add_player("3")
    se.add_player("4")
    se.add_player("5")
    se.add_player("6")
    se.add_player("7")
    se.add_player("8")
    se.add_player("9")
    se.add_player("10")
    se.add_player("11")
    se.add_player("12")
    se.add_player("13")
    se.add_player("14")
    # se.add_player("15")
    print(se.start_tournament())

    # print(se.get_initial_bracket())


if __name__ == "__main__":
    main()
    # test_rulesets()
