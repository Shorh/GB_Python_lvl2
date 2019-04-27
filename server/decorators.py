import logging

from functools import wraps

from protocol import make_403


logger = logging.getLogger('decorators')


def logged(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        logger.debug(f'{ func.__name__ }: { request }')
        return func(request, *args, **kwargs)

    return wrapper


def login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.get('user').get('username'):
            return func(request, *args, **kwargs)
        return make_403(request)

    return wrapper
