import discord


class Player:
    def __init__(self, user):
        self.user = user
        self.name = user.display_name
        self.current_match = None
        self.mention = user.mention
        self.id = user.id

        self.match_history = []
        self.valid = True

        self.rank = None

    def get_history(self):
        return self.match_history

    def update_match(self, result: bool):
        self.match_history.append(self.current_match)
        self.current_match = None

        if not result:
            self.valid = False

    def get_opponent(self):
        """
            Shown the opponent for the player's current match
        """

        if not self.valid:
            return "You are out of the tournament!"

        match = self.current_match
        if match.player_one == self:
            if match.player_two:
                return "Your next opponent is {0}".format(match.player_two)
            else:
                match = match.right_match
                return "Your next opponent is the winner of {0} vs {1}".format(
                    match.player_one, match.player_two,
                )
        else:
            if match.player_one:
                return "Your next opponent is {0}".format(match.player_one)
            else:
                match = match.left_match
                return "Your next opponent is the winner of {0} vs {1}".format(
                    match.player_one, match.player_two,
                )

    def set_current_match(self, next_match):
        self.current_match = next_match

    def __str__(self):
        if not self.mention:
            return self.name

        return self.mention
