from ..rulesets import single_elimination as se


def func(x):
    return x + 1


def test_answer():
    assert func(3) == 4
