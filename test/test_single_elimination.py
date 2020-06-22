import discord
from ..rulesets.single_elimination import SingleElimination as se
from .mock.mock_member import MockMember

tournament = se()


def test_add_player():
    tournament = se()
    players = [MockMember("player0"), MockMember("player1"), MockMember("player2")]
    tournament.add_player(players[0])
    tournament.add_player(players[1])
    tournament.add_player(players[2])

    assert len(tournament.get_players()) == 3

    tournament.add_player(players[0])

    assert len(tournament.get_players()) == 3
    tournament_players = {player.name for player in tournament.get_players()}

    print(tournament_players)
    for player in players:
        assert player.display_name in tournament_players


def test_start_tournament():
    tournament = se()
    players = [MockMember("player" + str(i)) for i in range(8)]

    assert tournament.start_tournament() == (None, False)

    tournament.add_player(players[0])
    assert tournament.start_tournament() == (None, False)

    tournament.add_player(players[1])
    bracket = "[player0]  \n" + "        |--\n" + "[player1]  \n"

    assert tournament.start_tournament(False) == (bracket, True)

    tournament.add_player(players[2])
    bracket = (
        "[player0]  \n"
        + "        |--|\n"
        + "[player1]  |\n"
        + "           |--|\n"
        + "[player2]  |\n"
        + "        |--|\n"
        + "[bye    ]  \n"
    )

    assert tournament.start_tournament(False) == (bracket, True)

    for i in range(3, 6):
        tournament.add_player(players[i])

    bracket = (
        "[player0]  \n"
        + "        |--|\n"
        + "[player1]  |\n"
        + "           |--|\n"
        + "[player2]  |  |\n"
        + "        |--|  |\n"
        + "[player3]     |\n"
        + "              |--\n"
        + "[player4]     |\n"
        + "        |--|  |\n"
        + "[bye    ]  |  |\n"
        + "           |--|\n"
        + "[player5]  |\n"
        + "        |--|\n"
        + "[bye    ]  \n"
    )

    assert tournament.start_tournament(False) == (bracket, True)

    tournament.add_player(players[6])
    tournament.add_player(players[7])

    bracket = (
        "[player0]  \n"
        + "        |--|\n"
        + "[player1]  |\n"
        + "           |--|\n"
        + "[player2]  |  |\n"
        + "        |--|  |\n"
        + "[player3]     |\n"
        + "              |--\n"
        + "[player4]     |\n"
        + "        |--|  |\n"
        + "[player5]  |  |\n"
        + "           |--|\n"
        + "[player6]  |\n"
        + "        |--|\n"
        + "[player7]  \n"
    )

    assert tournament.start_tournament(False) == (bracket, True)

def test_update_match():
    tournament = se()

    for i in range(6):
        tournament.add_player(MockMember("player" + str(i)))

    tournament.start_tournament(False)

    tournament.update_match(2, 1)
    tournament.update_match(4, 0)

    test_match_summary = {'3: player0 vs. player1 level: 2', '1: None vs. player2 level: 1', '0: None vs. player5 level: 0'}
    actual_match_summary = [match.summary() for _, match in tournament.valid_matches.items()]

    for match in actual_match_summary:
        assert match in test_match_summary

def test_end_game():
    tournament = se()

    for i in range(4):
        tournament.add_player(MockMember("player" + str(i)))

    tournament.start_tournament(False)

    assert tournament.update_match(1, 1) == None
    assert tournament.update_match(2, 0) == None
    assert tournament.update_match(0, 0).name == "player1"
