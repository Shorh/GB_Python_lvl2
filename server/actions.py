from functools import reduce
from settings import INSTALLED_MODULES


def get_server_actions():
    return reduce(
        lambda value, item: value + getattr(item, 'action_names', []),
        reduce(
            lambda value, item: value + (getattr(item, 'actions', tuple()),),
            reduce(
                lambda value, item: value + (__import__(f'{item}.actions'),),
                INSTALLED_MODULES,
                tuple(),
            ),
            tuple(),
        ),
        [],
    )


def resolve(action, action_names=None):
    for item in action_names or get_server_actions():
        if item.get('action') == action:
            return item.get('controller')

    return None
