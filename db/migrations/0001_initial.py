# Generated by Django 4.2.7 on 2023-11-26 21:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=16, unique=True)),
                ('alias', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('is_read', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(choices=[('invitation', 'Invitation'), ('system', 'System Notification')], default='system', max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, unique=True)),
                ('possible_values', models.CharField(choices=[('N', 'Numeric'), ('P', 'Percentage')], default='N', max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='System',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
                ('description', models.TextField()),
                ('number_of_devices', models.PositiveIntegerField(default=0)),
                ('number_of_users', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('surname', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('creator', 'Creator'), ('user', 'User'), ('broker', 'Broker')], default='user', max_length=10)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserSystems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('system', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='systems_from_user', to='db.system')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_with_systems', to='db.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='UserDevices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='devices_from_user', to='db.device')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_with_devices', to='db.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='SystemDevices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='devices_in_system', to='db.device')),
                ('system', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='system_with_devices', to='db.system')),
            ],
        ),
        migrations.AddField(
            model_name='system',
            name='admin',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='system_admin', to='db.userprofile'),
        ),
        migrations.CreateModel(
            name='DeviceParameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='device_with_parameters', to='db.device')),
                ('parameter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parameter_in_device', to='db.parameter')),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='created_by_user', to='db.userprofile'),
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('notification_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='db.notification')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_invitations', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_invitations', to=settings.AUTH_USER_MODEL)),
                ('system', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='db.system')),
            ],
            bases=('db.notification',),
        ),
    ]