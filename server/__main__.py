import json
import yaml
import socket
import argparse
import time

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

    print('Сервер запущен')

    while True:
        client, address = sock.accept()
        print(f'Клиент с адресом { address } зафиксирован')

        time_req = time.ctime(time.time())

        b_data = client.recv(buffer_size)
        request = json.loads(b_data.decode(encoding))

        response = json.dumps(
            {
                'response': 'Пользователь: ' + request['user']['username'] + '. Статус: ' + request['user']['status'],
                'time': time_req
            }
        )
        client.send(response.encode(encoding))

        client.close()
except KeyboardInterrupt:
    print('Сервер остановлен')
