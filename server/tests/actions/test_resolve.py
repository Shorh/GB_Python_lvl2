import pytest

from actions import resolve
from presence.actions import get_presence


@pytest.fixture
def action():
    return 'presence'


@pytest.fixture
def assert_controllers():
    return get_presence


def test_resolve(action, assert_controllers):
    controllers = resolve(action)

    assert assert_controllers == controllers
