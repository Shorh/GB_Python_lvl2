import logging

from logging.handlers import TimedRotatingFileHandler

from settings import ENCODING


# Объект-логгер. Имя: server
logger = logging.getLogger('client')

# Объект форматирования
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(module)s - %(message)s'
)

# Файловый обработчик логирования
handler = TimedRotatingFileHandler('client_log_config.log',
                                   encoding=ENCODING,
                                   when='D',
                                   backupCount=3)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)

# Добавляем в логгер новый обработчик событий
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
