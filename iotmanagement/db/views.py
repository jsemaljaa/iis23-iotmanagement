from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from .decorators import admin_required


from .forms import *
from . import models

# Create your views here.


@admin_required
def admin_dashboard(request):
    users = User.objects.all()
    devices = models.Device.objects.all()
    systems = models.System.objects.all()
    return render(request, 'admin_dashboard.html', {'users': users, 'devices': devices, 'systems': systems})


@admin_required
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, instance=user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('user_detail', pk=pk)
    else:
        form = UserProfileEditForm(instance=user.userprofile)
    return render(request, 'user_edit.html', {'form': form, 'user': user})



def users_list(request):
    pass

@admin_required
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'user_detail.html', {'user': user})


def change_password(request):
    pass


def profile_delete(request):
    pass


@login_required
def profile_edit(request):
    user_profile = request.user.userprofile

    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()  # This will either create a new record or update an existing one
            return redirect('profile')  # Redirect to the edit profile page after saving changes
    else:
        form = UserProfileEditForm(instance=user_profile)

    return render(request, 'profile_edit.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    user_profile, created = models.UserProfile.objects.get_or_create(user=user)

    return render(request, 'profile.html', {'user': user, 'user_profile': user_profile})


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')  # Change 'dashboard' to the desired page after login
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('home')


def signup(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.user = form.cleaned_data['username']
            user.save()

            # Log in the user immediately after registration
            auth_login(request, user)

            # Redirect to the edit profile page
            return redirect('profile_edit')  # Change 'edit_profile' to the actual URL or name of your edit profile page
    else:
        form = UserProfileForm()

    return render(request, 'signup.html', {'user_profile_form': form})


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
    if request.method == 'POST':
        form = CreateHomeForm(request.POST)
        if form.is_valid():
            system = form.save(commit=False)
            system.number_of_devices = 0  # Set default number of devices
            system.number_of_users = 0    # Set default number of users
            system.save()
            return redirect('systems_list')
    else:
        form = CreateHomeForm()
    return render(request, 'system_create.html', {'form': form})


def systems_list(request):
    systems = models.System.objects.all()  # This should retrieve all System objects from the database
    context = {'systems': systems}
    return render(request, 'systems_list.html', context)


def system_delete(request, pk):
    system = get_object_or_404(models.System, pk=pk)
    if request.method == 'POST':  # Confirm that the form has been submitted
        system.delete()
        return redirect('systems_list')  # Redirect to the systems list page after deletion
    return render(request, 'system_confirm_delete.html', {'system': system})



def system_detail(request):
    pass


def system_edit(request, pk):  # 'pk' parameter must be expected here
    system = get_object_or_404(models.System, pk=pk)
    if request.method == 'POST':
        form = CreateHomeForm(request.POST, instance=system)
        if form.is_valid():
            form.save()
            return redirect('systems_list')
    else:
        form = CreateHomeForm(instance=system)
    return render(request, 'system_edit.html', {'form': form})


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
    context = {}

    if request.user.is_authenticated:
        # If logged in, include the username in the context
        context['username'] = request.user.username

    return render(request, 'home.html', context)