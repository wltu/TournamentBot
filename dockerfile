FROM python:3.8-alpine

LABEL maintainer="tu.willy.97@gmail.com"

WORKDIR /TournamentBot

COPY requirements.txt .

RUN apk update && \
    apk add ffmpeg build-base libffi-dev

RUN python3 -m pip install -U discord.py[voice] && \ 
    python -m pip install --upgrade pip && \
    pip install -r requirements.txt

COPY tournament_bot.py .
COPY __init__.py .
COPY cogs cogs
COPY rulesets rulesets
COPY test test
COPY sound sound

CMD pytest
# CMD tail -f /dev/null
