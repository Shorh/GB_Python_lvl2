import pytest

from datetime import datetime
from presence.controllers import get_presence


@pytest.fixture
def action_name():
    return 'presence'


@pytest.fixture
def user():
    print('Connected')
    return {
        'username': 'shorh',
        'status': 'on-line'
    }


@pytest.fixture
def time():
    return datetime.now().timestamp()


@pytest.fixture
def data():
    print('Connected')
    return 'Пользователь: shorh. Статус: on-line'


@pytest.fixture
def code():
    return 200


@pytest.fixture
def valid_request(action_name, user, time):
    return {
        'action': action_name,
        'user': user,
        'time': time,
    }


@pytest.fixture
def assert_response(action_name, user, time, data, code):
    return {
        'action': action_name,
        'user': user,
        'time': time,
        'data': data,
        'code': code
    }


def test_get_presence(valid_request, assert_response):
    response = get_presence(valid_request)

    for name, value in response.items():
        if name != 'time':
            assert assert_response.get('name') == response.get('name')
