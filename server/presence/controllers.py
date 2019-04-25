from protocol import make_response
from decorators import logged


@logged
def get_presence(request):
    username = request.get('user').get('username')
    status = request.get('user').get('status')

    data = f'Пользователь: {username}. Статус: {status}'

    return make_response(request, 200, data)
