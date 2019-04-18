import pytest

from datetime import datetime
from protocol import make_response


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
    return 400


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


def test_make_response(valid_request, code, data, assert_response):
    response = make_response(valid_request, code, data)

    for name, value in response.items():
        if name != 'time':
            assert assert_response.get('name') == response.get('name')
