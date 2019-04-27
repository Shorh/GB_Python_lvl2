import pytest
import json
import zlib

from datetime import datetime
from handlers import handle_default_request
from settings import ENCODING


@pytest.fixture
def action_name():
    return 'presence'


@pytest.fixture
def user():
    return {
        'username': 'shorh',
        'status': 'on-line',
        'token': '1'
    }


@pytest.fixture
def time():
    return datetime.now().timestamp()


@pytest.fixture
def data():
    return 'Пользователь: shorh. Статус: on-line'


@pytest.fixture
def code():
    return 200


@pytest.fixture
def valid_request(action_name, user, time):
    request = {
        'action': action_name,
        'user': user,
        'time': time,
    }
    return zlib.compress(json.dumps(request).encode(ENCODING))


@pytest.fixture
def assert_response(action_name, user, time, data, code):
    return {
        'action': action_name,
        'user': user,
        'time': time,
        'data': data,
        'code': code
    }


def test_make_valid_response(valid_request, assert_response):
    z_response = handle_default_request(valid_request)
    response = json.loads(zlib.decompress(z_response).decode(ENCODING))

    for name, value in response.items():
        if name != 'time':
            assert assert_response.get('name') == response.get('name')
