from datetime import datetime
from response import make_valid_response


def test_make_valid_response():
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

    response = make_valid_response(request)

    assert expected.get('data') == response.get('data')
