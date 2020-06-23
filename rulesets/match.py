from .enums import Bracket


class Match:
    def __init__(self, match_id, level=0, player_one=None, player_two=None):
        self.player_one = player_one
        self.player_two = player_two

        self.left_match = None
        self.right_match = None
        self.next_match = None
        self.level = level
        self.match_id = match_id

        if player_one:
            self.player_one.set_current_match(self)

        if player_two:
            self.player_two.set_current_match(self)

    def set_players(self, player_one, player_two):
        self.player_one = player_one
        self.player_two = player_two

        if player_one:
            self.player_one.set_current_match(self)

        if player_two:
            self.player_two.set_current_match(self)

    def set_next_match(self, next_match):
        self.next_match = next_match

    def update_player(self, prevous_match):
        if prevous_match == self.left_match:
            self.player_one = prevous_match.winner
            self.player_one.set_current_match(self)
            self.left_match = None

        if prevous_match == self.right_match:
            self.player_two = prevous_match.winner
            self.player_two.set_current_match(self)
            self.right_match = None

        # return self.right_match == None and self.left_match == None

    def update_match(self, winner_id):
        """ Update match results """
        if winner_id == self.player_one.id:
            self.winner = self.player_one
        elif winner_id == self.player_two.id:
            self.winner = self.player_two
        else:
            raise ValueError("Player id must be either one of the player in the match!")

        if self.player_one:
            self.player_one.update_match(self.winner == self.player_one)

        if self.player_two:
            self.player_two.update_match(self.winner == self.player_two)

        if self.next_match:
            self.next_match.update_player(self)

    def check_match(self):
        return self.player_one != None and self.player_two != None

    def set_matches(self, left_match=None, right_match=None):
        self.left_match = left_match
        self.right_match = right_match

        if left_match:
            left_match.set_next_match(self)
        if right_match:
            right_match.set_next_match(self)

    def get_players(self):
        return self.player_one, self.player_two

    def draw_bracket(self, name_length, connect_bracket):
        bracket = [
            self.get_player_name(self.player_one, name_length) + 2 * " ",
            " " * (name_length + 1) + "|--",
            self.get_player_name(self.player_two, name_length) + 2 * " ",
        ]

        if connect_bracket == Bracket.TOP:
            bracket[0] += "|"
            bracket[1] += "|"
        if connect_bracket == Bracket.DOWN:
            bracket[1] += "|"
            bracket[2] += "|"

        return bracket

    def summary(self):
        return "{0} vs. {1}".format(self.player_one, self.player_two)

    def detailed_summary(self):
        return "{0}: {1} vs. {2} - level {3}".format(
            self.match_id, self.player_one, self.player_two, self.level
        )

    def get_player_name(self, player, length):
        if player == None:
            name = "bye"
        else:
            name = player.name

        return "[" + name + " " * (length - len(name)) + "]"
