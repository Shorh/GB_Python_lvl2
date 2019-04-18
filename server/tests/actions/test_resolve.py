from actions import resolve
from presence.actions import get_presence


def test_resolve():
    action = 'presence'

    controllers = resolve(action)
    expected = get_presence

    assert expected == controllers
