class Match:
    def __init__(self,
                 player_a=None,
                 player_b=None):
        self.player_a = player_a
        self.player_b = player_b
        self.result = ""

        self.left_match = None
        self.right_match = None
        self.next_match = None

    def set_players(self, player_a, player_b):
        self.player_a = player_a
        self.player_b = player_b

    def set_next_match(self, next_match):
        self.next_match = next_match

    def update_player(self, prevous_match):
        if prevous_match == self.left_match:
            self.player_a = prevous_match.winner
            self.left_match = None

        if prevous_match == self.right_match:
            self.player_b = prevous_match.winner
            self.right_match = None

        return self.right_match == None and self.left_match == None

    def update_match(self, player):
        if player == 0:
            self.winner = self.player_a
        else:
            self.winner = self.player_b

        return self.next_match.update_player(self)

    def set_matches(self, left_match=None, right_match=None):
        self.left_match = left_match
        self.right_match = right_match

        if left_match:
            left_match.set_next_match(self)
        if right_match:
            right_match.set_next_match(self)

    def get_players(self):
        return self.player_a, self.player_b

    def draw_bracket(self, name_length, connect_bracket=0):
        bracket = [self._get_player_name(self.player_a, name_length) + 2 * ' ',
                   ' ' * (name_length + 1) + "|--",
                   self._get_player_name(self.player_b, name_length) + 2 * ' ']

        if connect_bracket == 1:
            bracket[0] += '|'
            bracket[1] += '|'
        if connect_bracket == 2:
            bracket[1] += '|'
            bracket[2] += '|'

        return bracket

    def summary(self):
        return str(self.player_a) + " vs. " +  str(self.player_b)

    def _get_player_name(self, player, length):
        return "[" + player + " "*(length - len(player)) + "]"


class LeafBracketMatch:
    def __init__(self, player, match, name_length):
        self.player = player
        self.match = match
        self.result = ""
        self.name_length = name_length

    def draw_bracket(self, connect_bracket=0):
        bracket = self.match.draw_bracket(2)

        bracket.append(' ' * (self.name_length + 4) + '|--')
        bracket.append(
            ' ' * 3 + self._get_player_name(self.player, self.name_length) + 2 * ' ')

        if connect_bracket != 0:
            bracket[3] += '|'
            bracket[4] += '|'

        return bracket

    def _get_player_name(self, player, length):
        return "[" + player + " "*(length - len(player)) + "]"
