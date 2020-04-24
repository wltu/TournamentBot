import random
from . import match


class SingleElimination:
    def __init__(self):
        self.num_players = 0
        self.players = []
        self.longest_player_name_length = 0

    def add_player(self, player_name):
        self.players.append(player_name)

    def get_players(self):
        return self.players

    def start_tournament(self):
        self._update_name_length()
        self.head_match = match.Match()
        queue = [self.head_match]
        bracket_size = 1
        size = 1
        random.shuffle(self.players)

        while len(self.players) >= 4 * bracket_size:
            current_match = queue.pop(0)
            left_match = match.Match()
            right_match = match.Match()

            current_match.set_matches(left_match, right_match)
            queue.append(left_match)
            queue.append(right_match)

            size -= 1

            if (size == 0):
                bracket_size *= 2
                size = bracket_size

        extra_players = len(self.players) - 2 * len(queue)
        player_index = 0
        self.valid_matches = {}
        self.match_index = 0

        for current_match in queue:
            if extra_players:
                left_match = match.Match(self.players[player_index],
                                        self.players[player_index + 1])
                right_match = None

                self.valid_matches[self.match_index] = left_match
                self.match_index += 1
                extra_players -= 1
                player_index += 2
                
                if(extra_players):
                    right_match = match.Match(self.players[player_index],
                                        self.players[player_index + 1])
                    extra_players -= 1
                    player_index += 2
                    self.valid_matches[self.match_index] = right_match
                    self.match_index += 1

                current_match.set_matches(left_match, right_match)

                if not right_match:
                    current_match.set_players(None,
                                          self.players[player_index])
                    player_index += 1
            else:
                current_match.set_players(
                    self.players[player_index],
                    self.players[player_index + 1]
                )

                self.valid_matches[self.match_index] = current_match
                self.match_index += 1

                player_index += 2

        print(len(queue))
        print(player_index)
        print(len(self.valid_matches))

    def update_match(self, match_index, player):
        if self.valid_matches[match_index].update_match(player):
            self.valid_matches[match_index] = self.valid_matches[match_index].next_match
        else:
            self.valid_matches.pop(match_index, None)

    def get_initial_bracket(self):
        # print(self.head_match.summary())
        self.print_summary(self.head_match)

        print("valid matches")

        for key, value in self.valid_matches.items():
            print(key)
            print(value.summary())

        print('Finish match 0 and 1')    
        self.update_match(0, 0)
        self.update_match(1, 0)
        for key, value in self.valid_matches.items():
            print(key)
            print(value.summary())

        return ""

    def print_summary(self, current_match):
        if current_match:
            print(current_match.summary())
            self.print_summary(current_match.left_match)
            self.print_summary(current_match.right_match)

    def _update_name_length(self):
        self.longest_player_name_length = 0
        for player_name in self.players:
            self.longest_player_name_length = max(
                len(player_name),
                self.longest_player_name_length)
