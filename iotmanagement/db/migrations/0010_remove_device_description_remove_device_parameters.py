# Generated by Django 4.2.7 on 2023-11-24 20:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0009_alter_parameter_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='description',
        ),
        migrations.RemoveField(
            model_name='device',
            name='parameters',
        ),
    ]
