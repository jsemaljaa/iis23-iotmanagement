# Generated by Django 4.2.7 on 2023-11-27 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0004_systemdeviceparameters'),
    ]

    operations = [
        migrations.AddField(
            model_name='systemdeviceparameters',
            name='value',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
