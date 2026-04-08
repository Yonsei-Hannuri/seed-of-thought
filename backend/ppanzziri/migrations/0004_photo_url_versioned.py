from django.db import migrations, models


def migrate_photo_url_forward(apps, schema_editor):
    BudgetRecord = apps.get_model('ppanzziri', 'BudgetRecord')
    for record in BudgetRecord.objects.exclude(photo_url=''):
        record.photo_url_original = record.photo_url
        record.save(update_fields=['photo_url_original'])


class Migration(migrations.Migration):

    dependencies = [
        ('ppanzziri', '0003_social'),
    ]

    operations = [
        migrations.AddField(
            model_name='budgetrecord',
            name='photo_url_original',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='budgetrecord',
            name='photo_url_compressed',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='budgetrecord',
            name='photo_url_resized',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.RunPython(migrate_photo_url_forward, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='budgetrecord',
            name='photo_url',
        ),
    ]
