# Generated by Django 4.2.7 on 2023-11-26 16:10

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("db", "0012_merge_20231125_1512"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="system",
            name="users",
        ),
        migrations.DeleteModel(
            name="SystemUsers",
        ),
    ]