from datetime import datetime
from protocol import make_response


def test_make_response():
    action_name = 'msg'
    user = {
        'username': 'shorh',
        'status': 'on-line'
    }
    data = 'Some data'
    code = 400

    request = {
        'action': action_name,
        'user': user,
        'time': datetime.now().timestamp(),
    }

    expected = {
        'action': action_name,
        'user': user,
        'time': None,
        'data': data,
        'code': code
    }

    response = make_response(request, code, data)

    assert expected.get('data') == response.get('data')
