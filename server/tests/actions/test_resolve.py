from actions import resolve
from presence.actions import get_presence
from actions import get_server_actions


def test_resolve():
    action = 'presence'
    server_actions = get_server_actions()

    controllers = resolve(action)
    expected = get_presence

    assert expected == controllers
