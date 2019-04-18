from datetime import datetime
from presence.controllers import get_presence


def test_get_presence():
    action_name = 'presence'
    user = {
        'username': 'shorh',
        'status': 'on-line'
    }
    data = 'Пользователь: shorh. Статус: on-line'
    code = 200

    request = {
        'action': action_name,
        'user': user,
        'time': datetime.now().timestamp()
    }

    expected = {
        'action': action_name,
        'user': user,
        'time': None,
        'data': data,
        'code': code
    }

    response = get_presence(request)

    for name, value in response.items():
        if name != 'time':
            assert expected.get('name') == response.get('name')
