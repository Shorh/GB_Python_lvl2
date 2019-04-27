import logging
import json

from actions import (
    resolve, get_server_actions
)
from protocol import (
    validate_request, make_response, make_400, make_404
)
from settings import ENCODING


def handle_default_request(row_request):
    request = json.loads(row_request.decode(ENCODING))

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

    row_response = json.dumps(response).encode(ENCODING)
    return row_response
