from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ppanzziri', '0004_photo_url_versioned'),
    ]

    operations = [
        migrations.CreateModel(
            name='WritingRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('char_count', models.PositiveIntegerField()),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('analysis_status', models.CharField(
                    choices=[('pending', 'Pending'), ('done', 'Done')],
                    default='pending',
                    max_length=10,
                )),
            ],
            options={
                'db_table': 'writing_records',
                'ordering': ['-submitted_at'],
            },
        ),
    ]
