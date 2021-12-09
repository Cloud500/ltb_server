from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm


def index(request):
    """
    TODO: Docstring

    :param request:
    :return:
    """
    message = ""

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                else:
                    message = 'Disabled account'
            else:
                message = 'Benutzername/Passwort nicht korrekt'
        else:
            is_logout = bool(request.POST.get('logout', False)) or False
            if is_logout:
                logout(request)
    else:
        form = LoginForm()
    return render(request, 'index.html', {'form': form,
                                          'message': message
                                          })
