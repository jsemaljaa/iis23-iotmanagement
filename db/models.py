from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField

# Create your models here.


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('creator', 'Creator'),
        ('user', 'User'),
        ('broker', 'Broker'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    email = models.EmailField()
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return f"{self.name} {self.surname} ({self.role})"

    def is_admin(self):
        return self.role.lower() == 'admin'

    def is_creator(self):
        return self.role.lower() == 'creator'

    def is_broker(self):
        return self.role.lower() == 'broker'

    def is_user(self):
        return self.role.lower() == 'user'


class Parameter(models.Model):
    class PossibleValue(models.TextChoices):
        NUMERIC = "N", _("Numeric")
        PERCENTAGE = "P", _("Percentage")

    name = models.CharField(max_length=16, unique=True)
    possible_values = models.CharField(
        max_length=16,
        choices=PossibleValue.choices,
        default=PossibleValue.NUMERIC
    )

    def __str__(self):
        return self.name


class Device(models.Model):
    identifier = models.CharField(max_length=16, unique=True, blank=False)
    alias = models.CharField(max_length=8)
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='created_by_user', default=1)

    def __str__(self):
        return f"{self.identifier}, added by: {self.created_by.user.username}"


class System(models.Model):
    name = models.CharField(max_length=16)
    description = models.TextField()
    number_of_devices = models.PositiveIntegerField(default=0)
    number_of_users = models.PositiveIntegerField(default=0)
    admin = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='system_admin', default=1)

    def __str__(self):
        return f"{self.name} {self.admin.user.username}"

    def get_absolute_url(self):
        return reverse('system_detail', args=[str(self.pk)])


class Notification(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    NOTIFICATION_TYPES = [
        ('invitation', 'Invitation'),
        ('system', 'System Notification'),
    ]
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='system')

    def __str__(self):
        return f"{self.get_type_display()}: {self.message}"


class Invitation(Notification):
    system = models.ForeignKey(System, on_delete=models.CASCADE)
    sender = models.ForeignKey(UserProfile, related_name='sent_invitations', on_delete=models.CASCADE)
    recipient = models.ForeignKey(UserProfile, related_name='received_invitations',
                                  on_delete=models.CASCADE)

    def accept(self):
        # Add recipient to the system, mark the notification as read, and delete the invitation
        relation = UserSystems(system=self.system, user=self.recipient)
        print(f"system: {self.system}, recipient: {self.recipient}")
        relation.save()
        # relation = UserSystems(system_id=self.system.id, user_id=self.user.id)
        # self.system.systems_from_user.add(relation, bulk=False)
        self.is_read = True
        self.message = f"Invitation to {self.system.name} accepted."
        self.save()
        self.delete()

    def decline(self):
        # Mark the notification as read, update the message, and delete the invitation
        self.is_read = True
        self.message = f"Invitation to {self.system.name} declined."
        self.save()
        self.delete()

    def __str__(self):
        # Specific string representation for Invitation instances
        return f"Invitation from {self.sender.username} to {self.recipient.username} for {self.system.name}"


class SystemDevices(models.Model):
    system = models.ForeignKey(System, on_delete=models.CASCADE, related_name='system_with_devices')
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='devices_in_system')


class UserSystems(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_with_systems')
    system = models.ForeignKey(System, on_delete=models.CASCADE, related_name='systems_from_user')


class DeviceParameter(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='device_with_parameters')
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, related_name='parameter_in_device')
    value = models.IntegerField()


class SystemDeviceParameters(models.Model):
    class Meta:
        unique_together = (('device', 'parameter', 'system'),)

    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='device_with_parameters_in_system')
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, related_name='parameter_in_device_in_system')
    system = models.ForeignKey(System, on_delete=models.CASCADE, related_name='system_with_devices_with_parameters')
    value = models.IntegerField()