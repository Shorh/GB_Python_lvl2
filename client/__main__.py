import json
import yaml
import socket
import argparse
import time
import logging

from logging.handlers import TimedRotatingFileHandler
from settings import (
    HOST, PORT, BUFFER_SIZE, ENCODING
)

host = HOST
port = PORT
buffer_size = BUFFER_SIZE
encoding = ENCODING

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
    handlers=[
        TimedRotatingFileHandler('client_log_config.log',
                                 encoding=ENCODING,
                                 when='D',
                                 backupCount=3)
    ]
)

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

    logging.info('Клиент запущен')
    username = input('Введите ваш логин: ')

    time_req = time.ctime(time.time())

    request = json.dumps(
        {
            'action': 'presence',
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

    logging.info(response)
    sock.close()
except KeyboardInterrupt:
    logging.info('Клиент остановлен')
