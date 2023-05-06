from django.shortcuts import redirect


def redirect_main(request):
    response = redirect('/news/')
    return response