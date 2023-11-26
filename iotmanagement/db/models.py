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


class Parameter(models.Model):
    class PossibleValue(models.TextChoices):
        """
            NUMERIC = "N", "Numeric"
            PERCENTAGE = "P", "Percentage"
            ON_OFF = "OO", "On/Off"
            STRING = "S", "String"
            BOOLEAN = "B", "Boolean"
            COLOR = "C", "Color"
            TIMESTAMP = "TS", "Timestamp"
            DURATION = "D", "Duration"
            DISTANCE = "DI", "Distance"
            WEIGHT = "W", "Weight"
            VOLTAGE = "V", "Voltage"
            CURRENT = "I", "Current"
            PRESSURE = "P", "Pressure"
            TEMPERATURE = "T", "Temperature"
            HUMIDITY = "H", "Humidity"
            SPEED = "SP", "Speed"
        """
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
    users = models.ManyToManyField(User, related_name='systems')
    admin = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='system_admin', default=1)

    def __str__(self):
        return f"{self.name} {self.admin.user.username} ({self.role})"

    def get_absolute_url(self):
        return reverse('system_detail', args=[str(self.pk)])


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_invitations', on_delete=models.CASCADE)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_invitations', on_delete=models.CASCADE)

    def accept(self):
        # Add recipient to the system, mark the notification as read, and delete the invitation
        self.system.users.add(self.recipient)
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


class SystemUsers(models.Model):
    system = models.ForeignKey(System, on_delete=models.CASCADE, related_name='system_with_users')
    user = models.ForeignKey(System, on_delete=models.CASCADE, related_name='users_in_system')


class UserDevices(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_with_devices')
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='devices_from_user')


class UserSystems(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_with_systems')
    system = models.ForeignKey(System, on_delete=models.CASCADE, related_name='systems_from_user')


class DeviceParameter(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='device_with_parameters')
    parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, related_name='parameter_in_device')
    value = models.IntegerField()

# class KPI(models.Model):
#     class Function(models.TextChoices):
#         GT = ">"
#         GE = ">="
#         LT = "<"
#         LE = "<="
#         EQ = "="
#         choices = (
#             (GT, "is greater than"),
#             (GE, "is greater or equal"),
#             (LT, "is less than"),
#             (LE, "is less or equal"),
#             (EQ, "is equal"),
#         )
#
#     function = models.CharField(choices=Function.choices, default=Function.EQ)
#     parameter = models.ForeignKey(Parameter, on_delete=models.CASCADE, related_name='parameter')

    # TODO ! ! !
    # kpi will look something like
    # if humidity (parameter) > 80 then false
    # idk if we even should implement it like a table







