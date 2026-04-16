from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ppanzziri', '0006_pushsubscription_writinggoal'),
    ]

    operations = [
        migrations.AddField(
            model_name='writingrecord',
            name='summary',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='writingrecord',
            name='keywords',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name='writingrecord',
            name='analyzed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
