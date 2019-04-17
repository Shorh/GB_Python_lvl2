import json
import yaml
import socket
import argparse

from actions import (
    resolve, get_server_actions
)
from protocol import (
    validate_request, make_response, make_400, make_404
)
from settings import (
    HOST, PORT, BUFFER_SIZE, ENCODING
)


host = HOST
port = PORT
buffer_size = BUFFER_SIZE
encoding = ENCODING

parser = argparse.ArgumentParser()
parser.add_argument(
    '-c', '--config', type=str,
    help='Sets run configuration'
)
parser.add_argument(
    '-p', '--port', type=str,
    help='Sets port'
)
parser.add_argument(
    '-a', '--address', type=str,
    help='Sets IP-address'
)
args = parser.parse_args()

if args.config:
    with open(args.config) as file:
        conf = yaml.load(file, Loader=yaml.Loader)
        host = conf.get('host', HOST)
        port = conf.get('port', PORT)
        buffer_size = conf.get('buffer_size', BUFFER_SIZE)
        encoding = conf.get('encoding', ENCODING)
if args.port:
    port = args.port
if args.address:
    host = args.address

try:
    sock = socket.socket()
    sock.bind((host, port))
    sock.listen(10)
    server_actions = get_server_actions()

    print('Сервер запущен')

    while True:
        client, address = sock.accept()
        print(f'Клиент с адресом {address} зафиксирован')

        b_request = client.recv(buffer_size)
        request = json.loads(b_request.decode(encoding))
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

        s_response = json.dumps(response)
        client.send(s_response.encode(encoding))

        client.close()
except KeyboardInterrupt:
    print('Сервер остановлен')
