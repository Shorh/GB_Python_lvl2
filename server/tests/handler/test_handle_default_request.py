import pytest
import json
import zlib

from datetime import datetime
from handlers import handle_default_request
from settings import ENCODING

from protocol import (
    make_404, make_400
)


@pytest.fixture
def action_name():
    return 'presence'


@pytest.fixture
def action_name_none():
    return None


@pytest.fixture
def action_name_invalid():
    return 'abc'


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
def time_none():
    return None


@pytest.fixture
def data():
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
def invalid_request_none_action(action_name_none, user, time):
    return {
        'action': action_name_none,
        'user': user,
        'time': time,
    }


@pytest.fixture
def invalid_request_none_time(action_name, user, time_none):
    return {
        'action': action_name,
        'user': user,
        'time': time_none,
    }


@pytest.fixture
def invalid_request_action(action_name_invalid, user, time):
    return {
        'action': action_name_invalid,
        'user': user,
        'time': time,
    }


@pytest.fixture
def assert_valid_response(action_name, user, time, data, code):
    return {
        'action': action_name,
        'user': user,
        'time': time,
        'data': data,
        'code': code
    }


@pytest.fixture
def assert_invalid_response_action(invalid_request_none_action):
    return make_400(invalid_request_none_action)


@pytest.fixture
def assert_invalid_response_time(invalid_request_none_time):
    return make_400(invalid_request_none_time)


@pytest.fixture
def assert_invalid_action(invalid_request_action):
    return make_404(invalid_request_action)


def test_handle_default_request_valid_response(
        valid_request,
        assert_valid_response
):
    request = zlib.compress(json.dumps(valid_request).encode(ENCODING))
    z_response = handle_default_request(request)
    response = json.loads(zlib.decompress(z_response).decode(ENCODING))

    for name, value in response.items():
        if name != 'time':
            assert assert_valid_response.get('name') == response.get('name')


def test_handle_default_request_invalid_response_action(
        invalid_request_none_action,
        assert_invalid_response_action
):
    request = zlib.compress(
        json.dumps(invalid_request_none_action).encode(ENCODING)
    )
    z_response = handle_default_request(request)
    response = json.loads(zlib.decompress(z_response).decode(ENCODING))

    for name, value in response.items():
        if name != 'time':
            assert assert_invalid_response_action.get('name') == \
                   response.get('name')


def test_handle_default_request_invalid_response_time(
        invalid_request_none_time,
        assert_invalid_response_time
):
    request = zlib.compress(
        json.dumps(invalid_request_none_time).encode(ENCODING)
    )
    z_response = handle_default_request(request)
    response = json.loads(zlib.decompress(z_response).decode(ENCODING))

    for name, value in response.items():
        if name != 'time':
            assert assert_invalid_response_time.get('name') == \
                   response.get('name')


def test_handle_default_request_invalid_action(
        invalid_request_action,
        assert_invalid_action
):
    request = zlib.compress(
        json.dumps(invalid_request_action).encode(ENCODING)
    )
    z_response = handle_default_request(request)
    response = json.loads(zlib.decompress(z_response).decode(ENCODING))

    for name, value in response.items():
        if name != 'time':
            assert assert_invalid_action.get('name') == \
                   response.get('name')
