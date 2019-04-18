import json
import yaml
import socket
import argparse
import logging

import log_config

from protocol import make_valid_response
from settings import (
    HOST, PORT, BUFFER_SIZE, ENCODING
)


host = HOST
port = PORT
buffer_size = BUFFER_SIZE
encoding = ENCODING

logger = logging.getLogger('server')

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

    logger.info('Сервер запущен')

    while True:
        client, address = sock.accept()
        logger.info(f'Клиент с адресом {address} зафиксирован')

        b_request = client.recv(buffer_size)
        request = json.loads(b_request.decode(encoding))

        response = make_valid_response(request)
        s_response = json.dumps(response)
        client.send(s_response.encode(encoding))

        client.close()
except KeyboardInterrupt:
    logger.info('Сервер остановлен')
