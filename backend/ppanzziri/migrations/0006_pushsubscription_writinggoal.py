from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ppanzziri', '0005_writingrecord'),
    ]

    operations = [
        migrations.CreateModel(
            name='PushSubscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('endpoint', models.TextField(unique=True)),
                ('p256dh', models.TextField()),
                ('auth', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'push_subscriptions',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='WritingGoal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_chars', models.PositiveIntegerField(default=1000)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'writing_goal',
            },
        ),
    ]
