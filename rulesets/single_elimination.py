import discord
import operator
import random
from .match import Match
from .enums import Bracket
from .player import Player


class SingleElimination:
    def __init__(self):
        self.num_players = 0
        self.players = []
        self.longest_player_name_length = 0
        self.player_map = {}
        self.all_matches = []
        self.match_index = 0
        self.valid_matches = {}

        self.ranking = []

    def add_player(self, user: discord.Member):
        id = user.id

        if id in self.player_map.keys():
            return False
        self.num_players += 1
        player = Player(user)

        self.player_map[id] = player
        self.players.append(player)

        return True

    def get_players(self):
        return self.players

    def get_opponent(self, player):
        if not self.player_map.get(player, None):
            return "You are not in the tournament"

        return self.player_map[player].get_opponent()

    def get_ranking(self, player=-1):
        if player >= 0:
            if not self.player_map[player].valid:
                return "{}'s rank in the tournament is {}".format(
                    self.player_map[player].name, self.player_map[player].rank
                )
            else:
                return "You are still in the tournament!"

        if len(self.ranking) == 0:
            return ""

        self.ranking.sort(key=operator.itemgetter(0, 1))
        ranks = ""
        for rank in self.ranking:
            ranks += "{0}: {1}".format(rank[0], rank[1]) + "\n"

        return ranks

    def get_history(self, player):
        if not self.player_map.get(player, None):
            return "You do not have match history for most recent tournament"

        history = self.player_map[player].get_history()

        if len(history) == 0:
            return "No match played yet."

        output = ""

        for match in history:
            p1 = match.player_one.name
            p2 = match.player_two.name
            winner = match.winner.name
            output += "{0} vs {1} : {2} won\n".format(p1, p2, winner)

        return output

    def start_tournament(self, shuffle=True):

        if len(self.players) < 2:
            return None, False
        self.ranking = []
        self._update_name_length()
        self.valid_matches = {}
        self.match_index = 0

        level = 0

        self.head_match = Match(self.match_index, level)
        self.all_matches = [self.head_match]

        self.match_index += 1
        level += 1

        queue = [self.head_match]
        bracket_size = 1
        size = 1

        if shuffle:
            random.shuffle(self.players)

        while len(self.players) >= 4 * bracket_size:
            current_match = queue.pop(0)
            left_match = Match(self.match_index, level)
            right_match = Match(self.match_index + 1, level)

            current_match.set_matches(left_match, right_match)
            queue.append(left_match)
            queue.append(right_match)

            self.all_matches.extend([left_match, right_match])
            self.match_index += 2

            size -= 1

            if not size:
                bracket_size *= 2
                size = bracket_size
                level += 1

        extra_players = len(self.players) - 2 * len(queue)
        has_extra = extra_players > 0
        player_index = 0

        self.valid_matches = {}

        for current_match in queue:
            if extra_players:
                left_match = Match(
                    self.match_index,
                    level,
                    self.players[player_index],
                    self.players[player_index + 1],
                )
                right_match = None
                self.valid_matches[left_match.match_id] = left_match
                self.all_matches.append(left_match)

                self.match_index += 1
                extra_players -= 1
                player_index += 2

                right_match = None
                if extra_players:
                    right_match = Match(
                        self.match_index,
                        level,
                        self.players[player_index],
                        self.players[player_index + 1],
                    )
                    extra_players -= 1
                    player_index += 2
                    self.valid_matches[right_match.match_id] = right_match
                    self.all_matches.append(right_match)
                    self.match_index += 1

                if not right_match:
                    right_match = Match(
                        self.match_index, level, self.players[player_index], None
                    )
                    self.match_index += 1
                    player_index += 1

                    self.all_matches.append(right_match)
                    self.valid_matches[right_match.match_id] = right_match

                current_match.set_matches(left_match, right_match)
            else:
                if not has_extra:
                    current_match.set_players(
                        self.players[player_index], self.players[player_index + 1]
                    )

                    self.valid_matches[current_match.match_id] = current_match
                else:
                    left_match = Match(
                        self.match_index, level, self.players[player_index], None
                    )
                    right_match = Match(
                        self.match_index + 1,
                        level,
                        self.players[player_index + 1],
                        None,
                    )

                    self.match_index += 2

                    current_match.set_matches(left_match, right_match)
                    self.all_matches.extend([left_match, right_match])

                    self.valid_matches[left_match.match_id] = left_match
                    self.valid_matches[right_match.match_id] = right_match

                player_index += 2

        bracket = self.get_initial_bracket()

        add_matches = []
        remove_matches = []
        for id in self.valid_matches:
            current_match = self.valid_matches[id]

            if not current_match.check_match():
                current_match.update_match(current_match.player_one.id)

                next_match = current_match.next_match

                add_matches.append(next_match)
                remove_matches.append(current_match)

        for current_match in remove_matches:
            self.valid_matches.pop(current_match.match_id, None)

        for current_match in add_matches:
            self.valid_matches[current_match.match_id] = current_match

        return bracket, True

    def update_match(self, match_index, winner_id):
        """ 
            Update Bracket Matches. Return the winner when tournament is over.
        """
        match = self.valid_matches[match_index]

        match.update_match(winner_id)
        rank = pow(2, match.level) + 1
        rank = min(rank, self.num_players)

        if winner_id == match.player_one.id:
            # player_one won
            match.player_two.rank = rank
            self.ranking.append((rank, match.player_two.name))
        else:
            # player_two won
            match.player_one.rank = rank
            self.ranking.append((rank, match.player_one.name))

        if match_index == 0:
            match.winner.rank = 1
            self.ranking.append((1, match.winner.name))

            return match.winner

        next_match = match.next_match
        self.valid_matches[next_match.match_id] = next_match
        self.valid_matches.pop(match_index, None)

        return None

    def get_initial_bracket(self):
        if len(self.all_matches) == 1:
            output = self.all_matches[0].draw_bracket(
                self.longest_player_name_length, Bracket.NONE
            )
        else:
            count = 0
            output = []
            update_index = []

            end = len(self.valid_matches) - 1
            for _, current_match in self.valid_matches.items():
                if count % 2:
                    x = current_match.draw_bracket(
                        self.longest_player_name_length, Bracket.TOP
                    )
                    output.extend(x)

                    if (count + 1) % 4:
                        if count != end:
                            output.append(
                                " " * (self.longest_player_name_length + 7) + "|--"
                            )
                    else:
                        output.append("")
                else:
                    x = current_match.draw_bracket(
                        self.longest_player_name_length, Bracket.DOWN
                    )
                    output.extend(x)

                    update_index.append(len(output))
                    output.append(" " * (self.longest_player_name_length + 4) + "|--")
                count += 1

            draw_line = False
            length = 0
            for i in range(len(output)):
                if not draw_line:
                    if i == update_index[0]:
                        draw_line = True
                        update_index.pop(0)
                        output[i] += "|"
                        length = len(output[i])
                else:
                    if i == update_index[0]:
                        draw_line = False
                        update_index.pop(0)
                        output[i] += "|"
                    elif len(output[i]) < length:
                        output[i] += " " * (length - len(output[i]) - 1) + "|"

                if len(update_index) == 0:
                    break

        output_string = ""

        for line in output:
            if len(line) > 0:
                output_string += line + "\n"

        # return output
        return output_string

    def print_summary(self, current_match):
        if current_match:
            print(current_match.summary())
            self.print_summary(current_match.left_match)
            self.print_summary(current_match.right_match)

    def _update_name_length(self):
        self.longest_player_name_length = 3
        for player in self.players:
            name = player.name
            self.longest_player_name_length = max(
                len(name), self.longest_player_name_length
            )
