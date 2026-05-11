from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ppanzziri', '0007_writingrecord_analysis_fields'),
    ]

    operations = [
        # Remove old content field
        migrations.RemoveField(
            model_name='writingrecord',
            name='content',
        ),
        # Add new fields to WritingRecord
        migrations.AddField(
            model_name='writingrecord',
            name='date',
            field=models.DateField(default='2026-01-01'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='writingrecord',
            name='start_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='writingrecord',
            name='end_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='writingrecord',
            name='timelapse_video_url',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='writingrecord',
            name='topics',
            field=models.JSONField(blank=True, default=list),
        ),
        # Update char_count default
        migrations.AlterField(
            model_name='writingrecord',
            name='char_count',
            field=models.PositiveIntegerField(default=0),
        ),
        # Update ordering
        migrations.AlterModelOptions(
            name='writingrecord',
            options={'ordering': ['-date', '-submitted_at']},
        ),
        # Create WritingManuscriptPhoto model
        migrations.CreateModel(
            name='WritingManuscriptPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo_url_original', models.TextField(blank=True, default='')),
                ('photo_url_compressed', models.TextField(blank=True, default='')),
                ('photo_url_resized', models.TextField(blank=True, default='')),
                ('order', models.PositiveIntegerField(default=0)),
                ('record', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='manuscript_photos',
                    to='ppanzziri.writingrecord',
                )),
            ],
            options={
                'db_table': 'writing_manuscript_photos',
                'ordering': ['order', 'id'],
            },
        ),
    ]
