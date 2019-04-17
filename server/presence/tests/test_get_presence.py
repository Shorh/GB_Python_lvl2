from datetime import datetime
from presence.controllers import get_presence


def test_get_presence():
    action_name = 'presence'
    data = 'Пользователь: shorh. Статус: on-line'

    request = {
        'action': action_name,
        'time': datetime.now().timestamp(),
        'user': {
            'username': 'shorh',
            'status': 'on-line'
        }
    }

    expected = {
        'action': action_name,
        'user': {
            'username': 'shorh',
            'status': 'on-line'
        },
        'time': None,
        'data': data,
        'code': 200
    }

    response = get_presence(request)

    assert expected.get('data') == response.get('data')
