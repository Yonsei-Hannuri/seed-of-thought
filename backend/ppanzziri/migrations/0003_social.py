from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ppanzziri', '0002_budgetrecord_memo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Social',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('youtube_embed_url', models.TextField(blank=True, default='')),
                ('instagram_post_url', models.TextField(blank=True, default='')),
                ('instagram_profile_url', models.TextField(blank=True, default='')),
                ('extra_links', models.JSONField(blank=True, default=list)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'social',
            },
        ),
    ]
