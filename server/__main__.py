import json
import yaml
import socket
import argparse
import logging

from logging.handlers import TimedRotatingFileHandler

from protocol import make_valid_response
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
        TimedRotatingFileHandler('server_log_config.log',
                                 encoding=ENCODING,
                                 when='D',
                                 backupCount=3),
    ]
)

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

        logging.info(f'host {host}')
        logging.info(f'port {port}')
        logging.info(f'buffer_size {buffer_size}')
        logging.info(f'encoding {encoding}')
if args.port:
    port = args.port
    logging.info(f'port {port}')
if args.address:
    host = args.address
    logging.info(f'host {host}')

try:
    sock = socket.socket()
    sock.bind((host, port))
    sock.listen(10)

    logging.info('Сервер запущен')

    while True:
        client, address = sock.accept()
        logging.info(f'Клиент с адресом {address} зафиксирован')

        b_request = client.recv(buffer_size)
        request = json.loads(b_request.decode(encoding))

        response = make_valid_response(request)
        s_response = json.dumps(response)
        client.send(s_response.encode(encoding))

        client.close()
except KeyboardInterrupt:
    logging.info('Сервер остановлен')
