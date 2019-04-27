import json
import yaml
import socket
import argparse
import hashlib
import zlib

from datetime import datetime
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
                                 backupCount=3),
        logging.StreamHandler()
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

    hash_obj = hashlib.sha256()
    hash_obj.update(
        str(datetime.now().timestamp()).encode(ENCODING)
    )

    username = input('Введите ваш логин: ')
    action = input('Введите имя action: ')

    time_req = datetime.now().timestamp()

    request = json.dumps(
        {
            'action': action,
            'time': time_req,
            'user': {
                'username': username,
                'status': 'on-line',
                'token': hash_obj.hexdigest()
            }
        }
    )

    sock.send(zlib.compress(request.encode(encoding)))
    b_data = sock.recv(buffer_size)

    b_response = zlib.decompress(b_data)

    response = json.loads(
        b_response.decode(encoding)
    )

    logging.info(response)
    sock.close()
except KeyboardInterrupt:
    logging.info('Клиент остановлен')
