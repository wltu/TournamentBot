# TournamentBot
Discord TournamentBot for setting up tournament in your own server.
![Python Windows](https://github.com/wltu/TournamentBot/workflows/Python%20Windows/badge.svg)
![Python Mac](https://github.com/wltu/TournamentBot/workflows/Python%20Mac/badge.svg)
![Python Linux](https://github.com/wltu/TournamentBot/workflows/Python%20Linux/badge.svg)

### Depedencies
 - [discord.py](https://github.com/Rapptz/discord.py)
 - [pytest](https://docs.pytest.org/en/stable/)
 - Python 3.5.3+

### Get Stared
To start the discord bot just do the following:
```
// Linux
python3 tournament_bot.py [TOKEN]
// Windows
py tournament_bot.py [TOKEN]
```

### Dockerfile
The dockerfile is availbe to build the docker image for the bot. By default the image will just run the pytest.

To start the discord bot consider the following:
```
docker run --rm [IMAGE] python3 tournament_bot.py [TOKEN]
```
