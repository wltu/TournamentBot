import discord
import argparse

from discord.ext import commands
from discord.utils import get

from rulesets import single_elimination
from rulesets import double_elimination
from rulesets import round_robin
from rulesets import ladder
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


if __name__ == "__main__":
    main()
