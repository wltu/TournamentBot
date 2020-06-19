import discord

class Player:
    def __init__(self, user : discord.Member):
        self.user = user
        self.name = user.display_name
        self.current_match = None

        self.match_history = []
        self.valid = True
    
    def update_match(self, result : bool):
        self.match_history.append(self.current_match)
        self.current_match = None

        if not result:
            self.valid = False

    def set_current_match(self, next_match):
        self.current_match = next_match
