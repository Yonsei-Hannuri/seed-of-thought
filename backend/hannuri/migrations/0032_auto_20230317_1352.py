# Generated by Django 3.2.5 on 2023-03-17 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hannuri', '0031_detgorireadtime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='permissionId',
        ),
        migrations.RemoveField(
            model_name='user',
            name='writerPermissioned',
        ),
    ]