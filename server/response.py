from actions import (
    resolve, get_server_actions
)
from protocol import (
    validate_request, make_response, make_400, make_404
)


def make_valid_response(request):
    server_actions = get_server_actions()
    action_name = request.get('action')

    if validate_request(request):
        controller = resolve(action_name, server_actions)
        if controller:
            try:
                response = controller(request)
            except Exception as err:
                print(err)
                response = make_response(
                    request, 500, 'Internal server error'
                )
        else:
            print(f'Action with name {action_name} does not exist')
            response = make_404(request)
    else:
        print(f'Request is no valid')
        response = make_400(request)

    return response
