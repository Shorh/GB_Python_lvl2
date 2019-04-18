from datetime import datetime
from protocol import validate_request


def test_validate_request():
    action_name = 'msg'

    request = {
        'action': action_name,
        'time': datetime.now().timestamp(),
    }

    expected = True

    response = validate_request(request)

    assert expected == response
