import pytest
from functools import reduce

from presence import actions as presence
from echo import actions as echo
from errors import actions as errors
from actions import get_server_actions


@pytest.fixture
def modules():
    return [
        echo,
        presence,
        errors,
    ]


@pytest.fixture
def assert_server_actions(modules):
    return reduce(
        lambda value, item: value + getattr(item, 'action_names', []),
        modules,
        []
    )


def test_get_server_actions(assert_server_actions):
    server_actions = get_server_actions()

    assert assert_server_actions == server_actions
