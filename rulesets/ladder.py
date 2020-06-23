class Ladder:
    def __init__(self):
        self.num_players = 0
        self.players = []
        self.longest_player_name_length = 0

    def add_player(self, player_name):
        pass

    def get_opponent(self, player):
        pass

    def get_ranking(self, player=-1):
        pass

    def get_history(self, player):
        pass

    def get_players(self):
        return self.players

    def start_tournament(self, shuffle=True):
        pass

    def update_match(self, match_index, winner_id):
        pass

    def get_initial_bracket(self):
        return ""

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
