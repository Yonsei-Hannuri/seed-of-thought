from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ppanzziri', '0008_writing_record_redesign'),
    ]

    operations = [
        migrations.AddField(
            model_name='writingrecord',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='writingrecord',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='writingrecord',
            name='place_name',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
