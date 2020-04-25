import random
from . import match

from .enums import Bracket

class SingleElimination:
    def __init__(self):
        self.num_players = 0
        self.players = []
        self.longest_player_name_length = 0
        self.players_to_match = {}
        self.all_matches = []
        self.match_index = 0

    def add_player(self, player_name):
        self.players.append(player_name)

    def get_players(self):
        return self.players

    def start_tournament(self):
        self._update_name_length()
        level = 0

        self.head_match = match.Match(self.match_index, level)
        self.all_matches = [self.head_match]

        self.match_index += 1
        level += 1

        queue = [self.head_match]
        bracket_size = 1
        size = 1
        random.shuffle(self.players)

        while len(self.players) >= 4 * bracket_size:
            current_match = queue.pop(0)
            left_match = match.Match(self.match_index, level)
            right_match = match.Match(self.match_index + 1, level)

            current_match.set_matches(left_match, right_match)
            queue.append(left_match)
            queue.append(right_match)

            self.all_matches.append(left_match)
            self.all_matches.append(right_match)

            self.match_index += 2

            size -= 1

            if (size == 0):
                bracket_size *= 2
                size = bracket_size
                level += 1

        extra_players = len(self.players) - 2 * len(queue)
        has_extra = extra_players > 0
        player_index = 0
        self.valid_matches = {}

        for current_match in queue:
            if extra_players:
                left_match = match.Match(self.match_index,
                                         level,
                                         self.players[player_index],
                                         self.players[player_index + 1])
                right_match = None
                self.valid_matches[left_match.match_id] = left_match
                self.all_matches.append(left_match)

                self.match_index += 1
                extra_players -= 1
                player_index += 2

                right_match = None
                if(extra_players):
                    right_match = match.Match(self.match_index,
                                              level,
                                              self.players[player_index],
                                              self.players[player_index + 1])
                    extra_players -= 1
                    player_index += 2
                    self.valid_matches[right_match.match_id] = right_match
                    self.all_matches.append(right_match)
                    self.match_index += 1

                if not right_match:
                    right_match = match.Match(self.match_index,
                                            level,
                                            self.players[player_index],
                                            None)
                    self.match_index += 1
                    player_index += 1

                    self.all_matches.append(right_match)
                    self.valid_matches[right_match.match_id] = right_match


                current_match.set_matches(left_match, right_match)
            else:
                if not has_extra:
                    current_match.set_players(
                        self.players[player_index],
                        self.players[player_index + 1]
                    )

                    self.valid_matches[current_match.match_id] = current_match
                else:
                    left_match = match.Match(self.match_index,
                                            level,
                                            self.players[player_index],
                                            None)
                    right_match = match.Match(self.match_index + 1,
                                            level,
                                            self.players[player_index + 1],
                                            None)

                    self.match_index += 2

                    current_match.set_matches(left_match, right_match)
                    self.all_matches.append(left_match)
                    self.all_matches.append(right_match)

                    self.valid_matches[left_match.match_id] = left_match
                    self.valid_matches[right_match.match_id] = right_match

                player_index += 2

        # print(len(queue))
        # print(player_index)
        # print(self.players)
        # print(len(self.valid_matches))
        # print(len(self.all_matches))

        # for x in self.all_matches:
        #     print(x.summary())
        
        # print()
        # for x in self.valid_matches:
        #     print(x)
        #     print(self.valid_matches[x].summary())

        return self.get_initial_bracket()


    def update_match(self, match_index, player):
        if self.valid_matches[match_index].update_match(player):
            self.valid_matches[match_index] = self.valid_matches[match_index].next_match
        else:
            self.valid_matches.pop(match_index, None)

    def get_initial_bracket(self):
        if len(self.all_matches) == 1:
            output = self.all_matches[0].draw_bracket(
                self.longest_player_name_length,
                Bracket.NONE)
        else:
            count = 0
            output = []
            update_index = []

            end = len(self.valid_matches) - 1
            for _, current_match in self.valid_matches.items():
                if count % 2:
                    x = current_match.draw_bracket(self.longest_player_name_length,
                                                Bracket.TOP)
                    output.extend(x)

                    if (count + 1) % 4:
                        if count != end:
                            output.append(
                                ' ' * (self.longest_player_name_length + 7) + '|--')
                    else:
                        output.append('')
                else:
                    x = current_match.draw_bracket(self.longest_player_name_length,
                                                Bracket.DOWN)
                    output.extend(x)

                    update_index.append(len(output))
                    output.append(
                        ' ' * (self.longest_player_name_length + 4) + '|--')
                count += 1

            draw_line = False
            length = 0
            for i in range(len(output)):
                if not draw_line:
                    if i == update_index[0]:
                        draw_line = True
                        update_index.pop(0)
                        output[i] += '|'
                        length = len(output[i])
                else:
                    if i == update_index[0]:
                        draw_line = False
                        update_index.pop(0)
                        output[i] += '|'
                    elif len(output[i]) < length:
                        output[i] += ' ' * (length - len(output[i]) - 1) + '|'

                if len(update_index) == 0:
                    break

        output_string = ""

        for line in output:
            output_string += line + '\n'

        return output_string

    def print_summary(self, current_match):
        if current_match:
            print(current_match.summary())
            self.print_summary(current_match.left_match)
            self.print_summary(current_match.right_match)

    def _update_name_length(self):
        self.longest_player_name_length = 3
        for player_name in self.players:
            self.longest_player_name_length = max(
                len(player_name),
                self.longest_player_name_length)
