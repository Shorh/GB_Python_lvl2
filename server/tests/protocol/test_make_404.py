from datetime import datetime
from protocol import make_404


def test_make_404():
    action_name = 'msg'
    user = None
    data = 'Action is not supported'
    code = 404

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

    response = make_404(request)

    for name, value in response.items():
        if name != 'time':
            assert expected.get('name') == response.get('name')
