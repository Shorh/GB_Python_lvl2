from functools import reduce
from settings import INSTALLED_MODULES


def get_server_actions():
    return reduce(
        lambda actions, module: actions + getattr(module, 'action_names', []),
        reduce(
            lambda submodules, module: submodules + (getattr(module, 'actions', tuple()),),
            reduce(
                lambda modules, module: modules + (__import__(f'{module}.actions'),),
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
