from django import forms
from django.forms import inlineformset_factory

from . import models
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User


class ChangePasswordForm(PasswordChangeForm):
    pass


class ParameterForm(forms.ModelForm):
    class Meta:
        model = models.Parameter
        fields = ['name', 'possible_values', 'value']


class UserProfileForm(UserCreationForm):
    # name = forms.CharField(max_length=50)
    # surname = forms.CharField(max_length=50)
    # location = forms.CharField(max_length=100)
    # email = forms.EmailField(max_length=50)

    class Meta:
        model = User
        fields = [
            'username',
            # 'name',
            # 'surname',
            # 'location',
            # 'email',
            'password1',
            'password2'
        ]


class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        fields = [
            'name',
            'surname',
            'location',
            'email',
            'role'
        ]

    def __init__(self, *args, **kwargs):
        super(UserProfileEditForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False


class DeviceForm(forms.ModelForm):
    class Meta:
        model = models.Device
        fields = [
            # TODO: device_type like relationship between parameter and device
            'identifier',
            'parameters',
            # 'description',
            'alias'
        ]

    def __init__(self, *args, **kwargs):
        super(DeviceForm, self).__init__(*args, **kwargs)
        # Customize the parameters field as a dropdown
        self.fields['parameters'].widget = forms.SelectMultiple(choices=YOUR_CHOICES_FROM_DATABASE)


class DeviceParameterForm(forms.ModelForm):
    class Meta:
        model = models.DeviceParameter
        fields = [
            'parameter',
            'value'
        ]



class CreateHomeForm(forms.ModelForm):
    class Meta:
        model = models.System
        fields = [
            'name',
            # 'description'
        ]


class SystemForm(forms.ModelForm):
    class Meta:
        model = models.System
        fields = ['name', 'description', 'number_of_devices', 'number_of_users']


