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
        fields = ['name', 'possible_values']

    def __init__(self, *args, **kwargs):
        super(ParameterForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = True

        self.fields['name'].widget = forms.TextInput(attrs={
            'placeholder': '(required)',
            'required': True,
        })
        self.fields['possible_values'].required = True

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if models.Parameter.objects.filter(name=name).exists():
            raise forms.ValidationError('A parameter with this name already exists.')
        return name


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

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'] = forms.CharField(
            label="Username",
            widget=forms.TextInput,
            error_messages={
                'unique': 'This username already exists'
            }
        )
        self.fields['password1'] = forms.CharField(
            label="Password",
            widget=forms.PasswordInput,
            error_messages={
                # 'required': 'Your custom required error message',
                'password_too_short': 'Your custom password is too short',
                'password_common': 'Your custom password is too common',
            }
        )

        self.fields['password2'] = forms.CharField(
            label="Password confirmation",
            widget=forms.PasswordInput,
        )


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
            'alias'
        ]

    def __init__(self, *args, **kwargs):
        super(DeviceForm, self).__init__(*args, **kwargs)
        self.fields['identifier'].required = True
        self.fields['identifier'].widget = forms.TextInput(attrs={
            'placeholder': '(required)',
            'required': True
        })
        self.fields['alias'].required = False
        self.fields['alias'].widget = forms.TextInput(attrs={
            'placeholder': '(optional)',
            'required': False
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


class SendInvitationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)

    def clean_username(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError(f"User with username {username} does not exist.")
        return username