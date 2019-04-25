from decorators import logged


@logged
def get_error(request):
    raise Exception('Some exception text')
