import discord
import argparse

from discord.ext import commands


def main():
    parser = argparse.ArgumentParser(description='Starting TournamentBot.')
    parser.add_argument('token', type=str,
                        help='discord bot token')

    args = parser.parse_args()

    # client = discord.Client()
    client = commands.Bot(command_prefix='!',
                          description='TournamentBot for your tournaments')

    @client.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(client))

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')

        await client.process_commands(message)

    @client.command()
    async def help(context, arg):

        await context.send(arg)

    @client.event
    async def on_command_error(content, error):
        if isinstance(error, commands.CommandNotFound):
            await content.channel.send(
                "Invalid commmands. Try `!help` to get more information!")
            return
        raise error

    client.run(args.token)


if __name__ == '__main__':
    main()
