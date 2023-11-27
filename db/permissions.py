from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import System

# Define needed permissions
content_type = ContentType.objects.get_for_model(System)
Permission.objects.create(codename='can_monitor_system', name='Can monitor system', content_type=content_type)
Permission.objects.create(codename='can_administrate_system', name='Can administrate system', content_type=content_type)
