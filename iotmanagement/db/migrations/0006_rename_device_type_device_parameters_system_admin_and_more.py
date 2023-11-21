# Generated by Django 4.2.7 on 2023-11-21 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0005_remove_system_admin_system_number_of_devices_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='device',
            old_name='device_type',
            new_name='parameters',
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
    ]
