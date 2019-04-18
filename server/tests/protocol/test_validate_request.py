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
def assert_response():
    return True


def test_validate_request(valid_request, assert_response):
    response = validate_request(valid_request)

    assert assert_response == response
