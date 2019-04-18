from datetime import datetime
from protocol import make_400


def test_make_400():
    action_name = 'msg'
    user = None
    data = 'Wrong request format'
    code = 400

    request = {
        'action': action_name,
        'time': datetime.now().timestamp(),
    }

    expected = {
        'action': action_name,
        'user': user,
        'time': None,
        'data': data,
        'code': code
    }

    response = make_400(request)

    assert expected.get('data') == response.get('data')

