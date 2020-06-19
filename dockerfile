FROM python:3.8-slim

LABEL maintainer="tu.willy.97@gmail.com"

WORKDIR /TournamentBot

RUN python3 -m pip install -U discord.py[voice] && \ 
    python -m pip install --upgrade pip && \
    pip install pytest

COPY tournament_bot.py .
COPY __init__.py .
COPY cogs cogs
COPY rulesets rulesets
COPY test test

CMD pytest
# CMD tail -f /dev/null
