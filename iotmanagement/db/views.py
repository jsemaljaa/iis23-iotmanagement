from django.http import HttpResponseForbidden, HttpResponse, JsonResponse
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

    return render(request, 'admin/dashboard.html', context)


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
    return render(request, 'admin/user_edit.html', context)


@user_passes_test(admin_required, login_url='login')
def user_delete(request, pk):
    user_to_delete = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user_to_delete.delete()
        return redirect('admin_dashboard')

    context = {
        'user_to_delete': user_to_delete
    }
    return render(request, 'admin/user_delete_confirm.html', context)


@user_passes_test(admin_required, login_url='login')
def user_detail(request, pk):
    user_to_display = get_object_or_404(User, pk=pk)
    context = {
        'user_to_display': user_to_display
    }
    return render(request, 'admin/user_detail.html', context)


@login_required(login_url='login')
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
    return render(request, 'profile/change_password.html', context)


@login_required(login_url='login')
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

    return render(request, 'profile/delete_confirm.html', context)


@login_required(login_url='login')
def profile_edit(request):
    user_profile, created = models.UserProfile.objects.get_or_create(user=request.user)

    if request.session.pop('user_just_created', False):
        messages.success(request, 'User successfully created!')

    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileEditForm(instance=user_profile)

    context = {
        'form': form
    }

    return render(request, 'profile/edit.html', context)


@login_required(login_url='login')
def profile(request):
    user = request.user
    user_profile, created = models.UserProfile.objects.get_or_create(user=user)

    context = {
        'user': user,
        'user_profile': user_profile
    }

    return render(request, 'profile/profile.html', context)


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()

    context = {
        'form': form
    }

    return render(request, 'login.html', context)


@login_required(login_url='login')
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

            messages.success(request, 'User created successfully!')
            request.session['user_just_created'] = True

            auth_login(request, user)

            return redirect('profile_edit')
    else:
        form = UserProfileForm()

    context = {
        'user_profile_form': form
    }

    return render(request, 'signup.html', context)


@login_required(login_url='login')
def devices_create(request):
    parameters = models.Parameter.objects.all()
    context = {
        'parameters': parameters
    }
    if request.method == 'POST':
        selected_parameters = request.session.get('device_selected_parameters', [])
        if 'device_selected_parameters' in request.session:
            del request.session['device_selected_parameters']

        device_form = DeviceForm(request.POST)
        parameter_form = ParameterForm(request.POST)

        context.update({
            'device_form': device_form,
            'parameter_form': parameter_form
        })

        if selected_parameters:
            if device_form.is_valid():
                device = device_form.save(commit=False)

                device.created_by = request.user.userprofile
                device.save()

                for parameter_id in selected_parameters:
                    parameter = models.Parameter.objects.get(id=parameter_id)
                    models.DeviceParameter.objects.create(device=device, parameter=parameter, value=0)

                return redirect('devices_list')

            else:
                print(device_form.errors)
                error_message = 'Invalid form data. Please check the form entries.'

                context.update({
                    'error_message_devices': error_message
                })

                return render(request, 'device/create.html', context)
        else:
            error_message = 'You have to select at least one parameter'
            context.update({
                'error_message_devices': error_message
            })

            return render(request, 'device/create.html', context)
    else:
        device_form = DeviceForm()
        parameter_form = ParameterForm()
        context.update({
            'device_form': device_form,
            'parameter_form': parameter_form
        })

    return render(request, 'device/create.html', context)


@login_required(login_url='login')
def parameter_delete(request):
    if request.method == 'POST':
        parameter_id = request.POST.get('parameter_id')
        parameter = get_object_or_404(models.Parameter, pk=parameter_id)
        parameter.delete()
        return JsonResponse({'success': True, 'message': 'Parameter deleted successfully'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})


@login_required(login_url='login')
def devices_list(request):
    devices = models.Device.objects.all()
    request.session['previous_page'] = request.path

    context = {
        'devices': devices
    }

    return render(request, 'device/list.html', context)


def devices_delete(request, pk):
    device = get_object_or_404(models.Device, id=pk)

    # Check if the user has permission to delete the device
    if device.created_by == request.user.userprofile:
        device.delete()

    return redirect('devices_list')


def devices_detail(request, pk):
    device = get_object_or_404(models.Device, id=pk, created_by=request.user.userprofile)

    device_parameters = models.DeviceParameter.objects.filter(device=device)

    print(device_parameters)

    parameters = [record.parameter for record in device_parameters]

    print(parameters)

    context = {
        'device': device,
        'parameters': parameters
    }

    return render(request, 'device/detail.html', context)


def devices_edit(request, pk):
    device = get_object_or_404(models.Device, pk=pk)

    if request.method == 'POST':
        form = DeviceForm(request.POST, instance=device)
        if form.is_valid():
            form.save()
            return redirect('devices_detail', pk=pk)  # Redirect to the detail page after editing
    else:
        form = DeviceForm(instance=device)

    return render(request, 'device/edit.html', {'form': form, 'device': device})


@login_required(login_url='/login/')
def system_create(request):
    if request.method == 'POST':
        form = CreateHomeForm(request.POST)
        if form.is_valid():
            new_system = form.save(commit=False)
            # Assuming you want to associate the home with the user
            print(new_system.admin)
            new_system.admin = request.user.userprofile
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
    query = request.GET.get('q', '')  # Get the query from the URL
    if query:
        # Filter systems where the name contains the query
        systems = models.System.objects.filter(name__icontains=query)
    else:
        systems = models.System.objects.all()

    return render(request, 'systems_list.html', {'systems': systems, 'query': query})


@login_required()
def system_delete(request, pk):
    system = get_object_or_404(models.System, pk=pk)
    if request.method == 'POST':  # Confirm that the form has been submitted
        system.delete()
        return redirect('systems_list')  # Redirect to the systems list page after deletion

    context = {
        'system': system
    }
    return render(request, 'system_delete.html', context)


def system_detail(request, pk):
    system = get_object_or_404(models.System, pk=pk)
    # Assuming 'users' and 'devices' are related names for related objects
    return render(request, 'system_detail.html', {'system': system})


@login_required()
def system_edit(request, pk):

    system = get_object_or_404(models.System, pk=pk)
    # if request.user != system.admin:
    #     return redirect('some_error_page')
    if request.method == 'POST':
        form = SystemForm(request.POST, instance=system)
        if form.is_valid():
            form.save()
            previous_page = request.session.get('previous_page', '/')
            return redirect(previous_page)  # Redirect to the list view
    else:
        form = SystemForm(instance=system)

        # Handle invite user form submission
    if 'email' in request.POST:
        email_to_invite = request.POST['email']
        # You should implement invite_user_to_system
        system_invite(request, email_to_invite, system)

        # Handle remove user form submission
    if 'remove_user' in request.POST:
        user_to_remove = User.objects.get(pk=request.POST['remove_user'])
        system.users.remove(user_to_remove)
        system.save()

    context = {
        'form': form
    }

    return render(request, 'system_edit.html', context)


@login_required
def system_remove_user(request, system_id, user_id):
    system = get_object_or_404(models.System, id=system_id)
    user_to_remove = get_object_or_404(models.User, id=user_id)

    # Check if the current user is the admin of the system
    if request.user != system.admin:
        # If not, do not allow them to remove users and return a forbidden response
        messages.error(request, "You do not have permission to remove users from this system.")
        return HttpResponseForbidden()

    # Check that the user to remove is not the admin
    if user_to_remove == system.admin:
        messages.error(request, "The admin of the system cannot be removed.")
        return redirect('system_detail', pk=system.pk)

    # Remove the user from the system
    system.users.remove(user_to_remove)
    system.save()

    # You can add a success message to the messages framework
    messages.success(request, f"{user_to_remove.username} was successfully removed from the system.")

    # Redirect to the system's detail page
    return redirect('system_detail', pk=system.pk)


def system_invite(request, pk):
    system = get_object_or_404(models.System, pk=system.pk)

    if request.method == 'POST':
        email = request.POST.get('email')
        # Here, implement your logic for inviting a user, which could include:
        # - Checking if the email already exists in the system
        # - Creating a new user or sending an invitation email with a signup link
        # - Associating the user with the system upon acceptance

        # For now, let's just print the email to the console (replace this with actual logic)
        print(f"Invite sent to {email}")

        # Redirect back to the system edit page
        return redirect('system_edit', pk=system.pk)

    return render(request, 'system_invite.html', {'system': system})


@login_required(login_url='login')
def parameter_create(request):
    if request.method == 'POST':
        form = ParameterForm(request.POST)
        if form.is_valid():
            parameter = form.save()
            parameters = models.Parameter.objects.all()



            return JsonResponse({'success': True, 'message': 'Parameter created successfully'})
        else:
            print("hello")
            error_message = form.errors.get('name', ['Unknown error'])[0]
            return JsonResponse({'success': False, 'error_message_parameters': error_message})
    else:
        return JsonResponse({'success': False, 'error_message': 'Invalid request method'})


@login_required(login_url='login')
def save_selected_parameters(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':

        selected_parameters = request.POST.getlist('selected_parameters[]', [])

        request.session['device_selected_parameters'] = selected_parameters

        # print(request.session['device_selected_parameters'])

        # print(request.session['device_selected_parameters'])

        return JsonResponse({'success': True, 'message': 'Selected parameters saved successfully'})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request'})


def home(request):
    context = {}

    if request.user.is_authenticated:
        context['username'] = request.user.username

    return render(request, 'home.html', context)
