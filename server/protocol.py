import logging

from datetime import datetime
from actions import (
    resolve, get_server_actions
)


def validate_request(raw):
    request_time = raw.get('time')
    request_action = raw.get('action')

    if request_time and request_action:
        return True

    return False


def make_response(request, code, data=None):
    return {
        'action': request.get('action'),
        'user': request.get('user'),
        'time': datetime.now().timestamp(),
        'data': data,
        'code': code
    }


def make_400(request):
    return make_response(request, 400, 'Wrong request format')


def make_404(request):
    return make_response(request, 404, 'Action is not supported')


def make_403(request):
    return make_response(request, 403, 'Access denied')


def make_valid_response(request):
    server_actions = get_server_actions()
    action_name = request.get('action')

    if validate_request(request):
        controller = resolve(action_name, server_actions)
        if controller:
            try:
                response = controller(request)
            except Exception as err:
                logging.critical(err)
                response = make_response(
                    request, 500, 'Internal server error'
                )
        else:
            logging.error(f'Action with name {action_name} does not exist')
            response = make_404(request)
    else:
        logging.error(f'Request is no valid')
        response = make_400(request)

    return response
