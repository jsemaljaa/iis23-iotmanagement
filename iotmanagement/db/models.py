from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings

# Create your models here.


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('creator', 'Creator'),
        ('user', 'User'),
        ('broker', 'Broker'),
        ('visitor', 'Visitor'),
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
    name = models.CharField(max_length=16)
    possible_values = models.CharField(max_length=16)
    value = models.IntegerField()


class Device(models.Model):
    identifier = models.CharField(max_length=16, unique=True)
    device_type = models.ManyToManyField(Parameter, related_name='device_type')
    description = models.TextField()
    alias = models.CharField(max_length=8)
    created_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='created_by_user', default=1)


class System(models.Model):
    name = models.CharField(max_length=16)
    description = models.TextField()
    number_of_devices = models.PositiveIntegerField(default=0)
    number_of_users = models.PositiveIntegerField(default=0)
    # admin = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='system_admin')

    def __str__(self):
        return f"{self.name} {self.admin.name} ({self.role})"

    def get_absolute_url(self):
        return reverse('system_detail', args=[str(self.pk)])


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







