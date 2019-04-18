import logging

from settings import ENCODING


# Объект-логгер. Имя: server
logger = logging.getLogger('server')

# Объект форматирования
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(module)s - %(message)s'
)

# Файловый обработчик логирования
handler = logging.FileHandler('server_log_config.log', encoding=ENCODING)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

# Добавляем в логгер новый обработчик событий
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
