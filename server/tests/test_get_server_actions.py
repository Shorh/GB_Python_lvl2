from functools import reduce

from presence import actions as presence
from echo import actions as echo
from actions import get_server_actions


def test_get_server_actions():
    modules = [
        echo,
        presence,
    ]

    server_actions = get_server_actions()
    expected = reduce(
        lambda value, item: value + getattr(item, 'action_names', []),
        modules,
        []
    )

    assert expected == server_actions

