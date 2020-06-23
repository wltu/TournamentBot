# TournamentBot
Discord TournamentBot for setting up tournament in your own server.

![Python Windows](https://github.com/wltu/TournamentBot/workflows/Python%20Windows/badge.svg)
![Python Mac](https://github.com/wltu/TournamentBot/workflows/Python%20Mac/badge.svg)
![Python Linux](https://github.com/wltu/TournamentBot/workflows/Python%20Linux/badge.svg)


The TournamentBot support basic music commands to join voice channel and play music from YouTube. The main functionility is to orgainize and host tournament within your discord server.

### Main Commands
```
The defuld command prefix is ! and are currently fixed.

end      End the current tournament and remove all the tournament voice 
         chanels.
history  Show your match history for current/most recent tournament.
matches  Show all ongoing matches in current tournament.
opponent Show the opponents for your next match. 
rank     Show your tournament rank along with overall ranks in the current
         tournament.
report   Report your match result for current tournament.
setup    Setup tournament.
signup   Signup for current tournament.
start    Start current tournament!
update   Update match resutre for current tournament. tournament Oragnizer 
         only.
```

### Supported Tournament Format
 - Single Elimination

## Development
### Depedencies
 - [discord.py](https://github.com/Rapptz/discord.py)
 - [pytest](https://docs.pytest.org/en/stable/)
 - [FPMG](https://www.ffmpeg.org/)
 - [opus](https://opus-codec.org/)
    - Reported only for non-windows and voice activities.
 - Python 3.5.3+

### Get Stared
To start the discord bot follow the commands below:
```
// Linux
python3 -m pip install -U discord.py[voice]
python3 -m pip install --upgrade pip
python3 tournament_bot.py [TOKEN]

// Windows
py -m pip install -U discord.py[voice]
py -m pip install --upgrade pip
py tournament_bot.py [TOKEN]
```

### Dockerfile
The dockerfile is availbe to build the docker image for the bot. By default the image will just run the pytest.

To start the discord bot follow the commands below:
```
docker run --rm [IMAGE] python3 tournament_bot.py [TOKEN]
```

## Future Works
 - Code Restructure
 - Tournament Format
    - Double Elimination
    - Round Robin
    - Ladder
 - Chain Multiple Tournament Events
 