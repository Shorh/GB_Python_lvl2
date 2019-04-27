import pytest

from actions import resolve
from presence.actions import get_presence


@pytest.fixture
def valid_action():
    return 'presence'


@pytest.fixture
def invalid_action():
    return 'abc'


@pytest.fixture
def assert_controllers():
    return get_presence


@pytest.fixture
def assert_false():
    return None


def test_resolve_valid_action(valid_action, assert_controllers):
    controllers = resolve(valid_action)

    assert assert_controllers == controllers


def test_resolve_invalid_action(invalid_action, assert_false):
    controllers = resolve(invalid_action)

    assert assert_false == controllers
