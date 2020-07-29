from decorators import logged, login_required


@logged
@login_required
def get_error(request):
    raise Exception('Some exception text')
