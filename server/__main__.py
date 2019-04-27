import yaml
import socket
import argparse
import logging
import select

from logging.handlers import TimedRotatingFileHandler

from handlers import handle_default_request
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
        logging.StreamHandler()
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

requests = []
connections = []

try:
    sock = socket.socket()
    sock.bind((host, port))
    sock.settimeout(0)
    sock.listen(10)

    logging.info('Сервер запущен')

    while True:
        try:
            client, address = sock.accept()
            logging.info(f'Клиент с адресом {address} зафиксирован')
            connections.append(client)
        except Exception:
            pass

        r_list, w_list, x_list = select.select(
            connections, connections, connections, 0
        )

        for r_client in r_list:
            b_request = r_client.recv(buffer_size)
            requests.append(b_request)

        if requests:
            b_request = requests.pop()
            b_response = handle_default_request(b_request)

            for w_client in w_list:
                w_client.send(b_response)
except KeyboardInterrupt:
    logging.info('Сервер остановлен')
