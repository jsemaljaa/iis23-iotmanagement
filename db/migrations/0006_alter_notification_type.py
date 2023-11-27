# Generated by Django 4.2.7 on 2023-11-27 20:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("db", "0005_alter_notification_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notification",
            name="type",
            field=models.CharField(
                choices=[
                    ("invitation", "Invitation"),
                    ("system", "System Notification"),
                    ("request", "Participation Request"),
                ],
                default="system",
                max_length=20,
            ),
        ),
    ]
