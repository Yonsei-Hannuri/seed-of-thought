# Generated by Django 3.2.5 on 2021-09-11 19:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hannuri', '0021_auto_20210911_1856'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='organizerPermissionId',
            new_name='writerPermissionId',
        ),
    ]
