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
            'identifier',
            'parameters',
            'alias'
        ]

    def __init__(self, *args, **kwargs):
        super(DeviceForm, self).__init__(*args, **kwargs)
        parameter_choices = models.Parameter.objects.values_list('name')
        self.fields['parameters'].widget = forms.SelectMultiple(choices=parameter_choices)
        self.fields['identifier'].required = False
        self.fields['identifier'].widget = forms.TextInput(attrs={
            'placeholder': 'Enter name',
            'required': 'True'
        })
        self.fields['alias'].required = False
        self.fields['alias'].widget = forms.TextInput(attrs={
            'placeholder': 'Enter Alias',
            'required': 'True'
        })



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


