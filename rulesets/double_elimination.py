class DoubleElimination:
    def __init__(self):
        self.num_players = 0
        self.players = []
        self.longest_player_name_length = 0

    def add_player(self, player_name):
        self.players.append(player_name)

    def get_players(self):
        return self.players

    def start_tournament(self):
        pass

    def get_initial_bracket(self):
        # bracket = ""
        # self._update_name_length()

        # # for player in self.players:
        # for i, player in enumerate(self.players):
        #     if (i % 2):
        #         bracket += " " * (self.longest_player_name_length + 2) + \
        #             "|---\n"
        #     elif (i > 0):
        #         bracket += "\n"

        #     bracket += self._get_player_name(player)

        bracket = []
        self._update_name_length()

        # for player in self.players:
        for i, player in enumerate(self.players):
            bracket.append(self._get_player_name(player))

            if i != len(self.players) - 1:
                bracket.append(" " * (self.longest_player_name_length + 2))

        bracket_output = ""

        for b in bracket:
            bracket_output += b + "\n"

        return bracket_output

    def _get_player_name(self, player):
        return (
            "[" + player + " " * (self.longest_player_name_length - len(player)) + "]"
        )

    def _update_name_length(self):
        self.longest_player_name_length = 0
        for player_name in self.players:
            self.longest_player_name_length = max(
                len(player_name), self.longest_player_name_length
            )
