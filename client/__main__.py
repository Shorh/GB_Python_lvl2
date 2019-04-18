import json
import yaml
import socket
import argparse
import time
import logging

import log_config

from settings import (
    HOST, PORT, BUFFER_SIZE, ENCODING
)

host = HOST
port = PORT
buffer_size = BUFFER_SIZE
encoding = ENCODING

logger = logging.getLogger('client')

parser = argparse.ArgumentParser()
parser.add_argument(
    '-c', '--config', type=str,
    help='Sets run configuration'
)
args = parser.parse_args()

if args.config:
    with open(args.config) as file:
        conf = yaml.load(file, Loader=yaml.Loader)
        host = conf.get('host', HOST)
        port = conf.get('port', PORT)
        buffer_size = conf.get('buffer_size', BUFFER_SIZE)
        encoding = conf.get('encoding', ENCODING)

try:
    sock = socket.socket()
    sock.connect((host, port))

    logger.info('Клиент запущен')
    username = input('Введите ваш логин: ')

    time_req = time.ctime(time.time())

    request = json.dumps(
        {
            'action': 'msg',
            'time': time_req,
            'user': {
                'username': username,
                'status': 'on-line'
            }
        }
    )

    sock.send(request.encode(encoding))
    b_data = sock.recv(buffer_size)

    response = json.loads(
        b_data.decode(encoding)
    )

    logger.info(response)
    sock.close()
except KeyboardInterrupt:
    logger.info('Клиент остановлен')
