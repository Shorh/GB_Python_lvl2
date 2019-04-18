from datetime import datetime
from echo.controllers import get_echo


def test_get_echo():
    action_name = 'echo'
    user = None
    data = 'Some data'
    code = 200

    request = {
        'action': action_name,
        'time': datetime.now().timestamp(),
        'data': data,
    }

    expected = {
        'action': action_name,
        'user': user,
        'time': None,
        'data': data,
        'code': code
    }

    response = get_echo(request)

    for name, value in response.items():
        if name != 'time':
            assert expected.get('name') == response.get('name')
