import pytest

from datetime import datetime
from protocol import validate_request


@pytest.fixture
def action_name():
    return 'msg'


@pytest.fixture
def time():
    return datetime.now().timestamp()


@pytest.fixture
def valid_request(action_name, time):
    return {
        'action': action_name,
        'time': time,
    }


@pytest.fixture
def invalid_request_action(action_name, time):
    return {
        'action': None,
        'time': time,
    }


@pytest.fixture
def invalid_request_time(action_name, time):
    return {
        'action': action_name,
        'time': None,
    }


@pytest.fixture
def assert_response_true():
    return True


@pytest.fixture
def assert_response_false():
    return False


def test_validate_request_true(valid_request, assert_response_true):
    response = validate_request(valid_request)

    assert assert_response_true == response


def test_validate_request_false_action(invalid_request_action, assert_response_false):
    response = validate_request(invalid_request_action)

    assert assert_response_false == response


def test_validate_request_false_time(invalid_request_time, assert_response_false):
    response = validate_request(invalid_request_time)

    assert assert_response_false == response
