from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import *
from . import models

# Create your views here.



def user_edit(request):
    pass


def users_list(request):
    pass


def user_detail(request):
    pass


def change_password(request):
    pass


def profile_delete(request):
    pass


def profile_edit(request):
    pass


def profile(request):
    pass


def login(request):
    pass


def signup(request):
    pass


def devices_create(request):
    pass


def devices_list(request):
    pass


def devices_delete(request):
    pass


def devices_detail(request):
    pass


def devices_edit(request):
    pass


def system_create(request):
    pass


def systems_list(request):
    systems = models.System.objects.all()

    visits = request.session.get('visits', 0)
    request.session['visits'] = visits + 1

    context = {
        "object": systems,
        'visits': visits
    }

    return render(request, 'systems_list.html', context=context)


def system_delete(request):
    pass


def system_detail(request):
    pass


def system_edit(request):
    pass


def parameter_create(request):
    if request.method == 'POST':
        form = ParameterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')
    else:
        form = ParameterForm()

    return render(request, 'parameter.html', {'form': form})


def home(request):
    # visits = request.session.get('visits', 0)
    # request.session['visits'] = visits + 1
    #
    # context = {
    #     "object": systems,
    #     'visits': visits
    # }

    return render(request, 'home.html')