# Generated by Django 3.2.5 on 2021-08-11 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hannuri', '0006_freenote'),
    ]

    operations = [
        migrations.RenameField(
            model_name='freenote',
            old_name='text',
            new_name='description',
        ),
    ]
