from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Parameter(models.Model):
    name = models.CharField(max_length=16)
    possible_values = models.CharField(max_length=16)
    value = models.IntegerField()


class Device(models.Model):
    identifier = models.CharField(max_length=16, unique=True)
    device_type = models.ManyToManyField(Parameter, related_name='device_type')
    description = models.TextField()
    alias = models.CharField(max_length=8)



class System(models.Model):
    name = models.CharField(max_length=16)
    description = models.TextField()
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='system_admin')
    users = models.ManyToManyField(User, related_name='system_users', blank=True)
    devices = models.ManyToManyField(Device, related_name='system_devices', blank=True);

    def get_absolute_url(self):
        return reverse('system_detail', args=[str(self.id)])

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




