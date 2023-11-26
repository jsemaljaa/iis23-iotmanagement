from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import get_user_model

from django.views.decorators.http import require_POST

from .forms import *
from . import models


# Misc helpers for views
def admin_required(user):
    return user.is_authenticated and user.userprofile.is_admin


def broker_required(user):
    return user.is_authenticated and user.userprofile.is_broker


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

    if request.user.userprofile.is_creator() or request.user.userprofile.is_admin():
        device = get_object_or_404(models.Device, id=pk, created_by=request.user.userprofile)

    if request.user.userprofile.is_broker():
        device = get_object_or_404(models.Device, id=pk)

    device_parameters = models.DeviceParameter.objects.filter(device=device)

    parameters = [record.parameter for record in device_parameters]
    values = [record.value for record in device_parameters]

    data = list(zip(parameters, values))

    for parameter, value in data:
        print(f"Parameter {parameter} with {value}")

    context = {
        'device': device,
        'data': data
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


@login_required(login_url='login')
def update_parameter(request, device_pk, parameter_pk):
    device_parameter = get_object_or_404(models.DeviceParameter, device_id=device_pk, parameter_id=parameter_pk)

    if request.method == 'POST':
        form = ModifyParameterForm(request.POST)
        if form.is_valid():
            device_parameter.value = form.cleaned_data['new_value']
            device_parameter.save()
            return JsonResponse({
                'success': True,
                'parameter_id': device_parameter.parameter.id,
                'new_value': device_parameter.value,
            })
        else:
            return JsonResponse({'success': False, 'error_message': 'Invalid form data'})

    return JsonResponse({'success': False, 'error_message': 'Invalid request method'})


@login_required(login_url='/login/')
def delete_parameter_from_device(request, device_id, parameter_id):
    device = get_object_or_404(models.Device, id=device_id)
    parameter = get_object_or_404(models.Parameter, id=parameter_id)

    deviceparameter = get_object_or_404(models.DeviceParameter, device=device, parameter=parameter)

    try:
        deviceparameter.delete()
        # device.parameters.remove(parameter)
        # parameter.delete()

        return redirect('devices_detail', pk=device.id)
    except Exception as e:
        return JsonResponse({'success': False, 'error_message': str(e)})



@login_required(login_url='/login/')
def system_create(request):
    if request.method == 'POST':
        form = CreateHomeForm(request.POST)
        if form.is_valid():
            new_system = form.save(commit=False)
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
    systems = models.System.objects.all()
    request.session['previous_page'] = request.path
    query = request.GET.get('q', '')
    if query:
        systems = models.System.objects.filter(name__icontains=query)
    else:
        systems = models.System.objects.all()
    context = {
        'systems': systems,
        'query': query
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
    return render(request, 'system_delete.html', context)


def system_detail(request, pk):
    system = get_object_or_404(models.System, pk=pk)
    return render(request, 'system_detail.html', {'system': system})


@login_required
def system_edit(request, pk):
    system = get_object_or_404(models.System, pk=pk)
    # if not system.users.filter(pk=request.user.pk).exists():
    #     messages.error(request, "You don't have permission to edit this system.")
    #     return redirect('systems_list')

    edit_form = SystemForm(instance=system)
    invite_form = SendInvitationForm()

    if request.method == 'POST':
        if 'edit_system' in request.POST:
            edit_form = SystemForm(request.POST, instance=system)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('system_detail', pk=system.pk)
        else:
            invite_form = SendInvitationForm(request.POST)
            if invite_form.is_valid():
                username = invite_form.cleaned_data['username']
                try:

                    user_to_invite = get_user_model().objects.get(username=username)
                    notification_message = f"You have been invited to {system.name}."
                    invitation = models.Invitation.objects.create(system=system, sender=request.user,
                                                                  user_id=user_to_invite.id,
                                                                  recipient=user_to_invite,
                                                                  user=user_to_invite, message=notification_message,
                                                                  is_read=False,
                                                                  type='invitation')


                    return redirect('system_edit', pk=system.pk)
                except get_user_model().DoesNotExist:
                    messages.error(request, f'User {username} does not exist.')
            return redirect('system_edit', pk=system.pk)

    return render(request, 'system_edit.html', {'system': system, 'edit_form': edit_form, 'invite_form': invite_form})



@login_required
def accept_invitation(request, notification_id):
    notification = get_object_or_404(models.Notification, id=notification_id)
    invitation = notification.invitation
    if request.method == 'POST':
        invitation.accept()
    return redirect('notifications')



@login_required
def decline_invitation(request, notification_id):
    notification = get_object_or_404(models.Notification, id=notification_id)
    invitation = notification.invitation
    if request.method == 'POST':
        invitation.decline()
    return redirect('notifications')


@login_required
def notifications(request):
    notifications = models.Notification.objects.filter(
        user=request.user,
        is_read=False
    )
    return render(request, 'notifications.html', {'notifications': notifications})


@login_required
def delete_notification(request, notification_id):
    notification = get_object_or_404(models.Notification, id=notification_id, user=request.user)

    if request.method == 'POST':
        notification.delete()
        return redirect('notifications')  # Redirect to the notifications page
    return redirect('notifications')

@login_required
def remove_user(request, system_id, user_id):
    system = get_object_or_404(models.System, pk=system_id)
    user = get_object_or_404(system.users, pk=user_id)
    system.users.remove(user)
    messages.success(request, f"User {user.username} has been removed from the system.")
    return redirect('system_edit', pk=system_id)


@login_required(login_url='login')
def parameter_create(request):
    if request.method == 'POST':
        form = ParameterForm(request.POST)
        if form.is_valid():
            parameter = form.save()
            # parameters = models.Parameter.objects.all()

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
