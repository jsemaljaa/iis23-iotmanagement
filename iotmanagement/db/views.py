from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages


from .forms import *
from . import models


# Misc helpers for views
def admin_required(user):
    return user.is_authenticated and user.userprofile.is_admin

# Create your views here.


@user_passes_test(admin_required, login_url='login')
def admin_dashboard(request):
    users = User.objects.all()
    devices = models.Device.objects.all()
    systems = models.System.objects.all()
    request.session['previous_page'] = request.path

    context = {
        'users': users,
        'devices': devices,
        'systems': systems
    }

    return render(request, 'admin_dashboard.html', context)


@user_passes_test(admin_required, login_url='login')
def user_edit(request, pk):
    user_to_edit = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, instance=user_to_edit.userprofile)
        if form.is_valid():
            form.save()
            return redirect('user_detail', pk=pk)
    else:
        form = UserProfileEditForm(instance=user_to_edit.userprofile)

    context = {
        'form': form,
        'user_to_edit': user_to_edit
    }
    return render(request, 'user_edit.html', context)


@user_passes_test(admin_required, login_url='login')
def user_delete(request, pk):
    user_to_delete = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user_to_delete.delete()
        return redirect('admin_dashboard')

    context = {
        'user_to_delete': user_to_delete
    }
    return render(request, 'user_delete_confirm.html', context)


@user_passes_test(admin_required, login_url='login')
def user_detail(request, pk):
    user_to_display = get_object_or_404(User, pk=pk)
    context = {
        'user_to_display': user_to_display
    }
    return render(request, 'user_detail.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
    else:
        form = ChangePasswordForm(request.user)

    context = {
        'form': form
    }
    return render(request, 'change_password.html', context)


@login_required
def profile_delete(request):
    user_profile = request.user.userprofile

    if request.method == 'POST':
        user = request.user
        user_profile.delete()
        user.delete()
        return redirect('home')

    context = {
        'user': user_profile
    }

    return render(request, 'profile_delete_confirm.html', context)


@login_required
def profile_edit(request):
    user_profile, created = models.UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()  # This will either create a new record or update an existing one
            return redirect('profile')  # Redirect to the edit profile page after saving changes
    else:
        form = UserProfileEditForm(instance=user_profile)

    context = {
        'form': form
    }

    return render(request, 'profile_edit.html', context)


@login_required
def profile(request):
    user = request.user
    user_profile, created = models.UserProfile.objects.get_or_create(user=user)

    context = {
        'user': user,
        'user_profile': user_profile
    }

    return render(request, 'profile.html', context)


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')  # Change 'dashboard' to the desired page after login
    else:
        form = AuthenticationForm()

    context = {
        'form': form
    }

    return render(request, 'login.html', context)


@login_required
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

    context = {
        'user_profile_form': form
    }

    return render(request, 'signup.html', context)


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


@login_required
def system_create(request):
    if request.method == 'POST':
        form = CreateHomeForm(request.POST)
        if form.is_valid():
            new_system = form.save(commit=False)
            # Assuming you want to associate the home with the user
            new_system.owner = request.user
            new_system.save()
            return redirect('systems_list')
    else:
        form = CreateHomeForm()

    context = {
        'form': form
    }

    return render(request, 'system_create.html', context)


def systems_list(request):
    systems = models.System.objects.all()  # This should retrieve all System objects from the database
    request.session['previous_page'] = request.path

    context = {
        'systems': systems
    }

    return render(request, 'systems_list.html', context)


@login_required()
def system_delete(request, pk):
    system = get_object_or_404(models.System, pk=pk)
    if request.method == 'POST':  # Confirm that the form has been submitted
        system.delete()
        return redirect('systems_list')  # Redirect to the systems list page after deletion

    context = {
        'system': system
    }

    return render(request, 'system_confirm_delete.html', context)


def system_detail(request, pk):
    pass


@login_required()
def system_edit(request, pk):
    system = get_object_or_404(models.System, pk=pk)
    if request.method == 'POST':
        form = SystemForm(request.POST, instance=system)
        if form.is_valid():
            form.save()
            previous_page = request.session.get('previous_page', '/')
            return redirect(previous_page)  # Redirect to the list view
    else:
        form = SystemForm(instance=system)

    context = {
        'form': form
    }

    return render(request, 'system_edit.html', context)


def parameter_create(request):
    if request.method == 'POST':
        form = ParameterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_page')
    else:
        form = ParameterForm()

    context = {
        'form': form
    }

    return render(request, 'parameter.html', context)


def home(request):
    context = {}

    if request.user.is_authenticated:
        # If logged in, include the username in the context
        context['username'] = request.user.username

    return render(request, 'home.html', context)
