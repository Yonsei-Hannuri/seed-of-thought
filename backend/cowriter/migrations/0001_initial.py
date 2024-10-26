# Generated by Django 3.2.5 on 2024-08-17 13:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Essay',
            fields=[
                ('created_dt', models.DateTimeField(auto_now_add=True, db_column='CREATED_DT', null=True)),
                ('updated_dt', models.DateTimeField(auto_now=True, db_column='UPDATED_DT', null=True)),
                ('essay_id', models.AutoField(db_column='ESSAY_ID', primary_key=True, serialize=False, verbose_name='에세이ID')),
                ('essay_title', models.CharField(blank=True, db_column='ESSAY_TITLE', max_length=200, verbose_name='제목')),
                ('owner', models.CharField(db_column='OWNER_ID', max_length=100, verbose_name='사용자')),
                ('complete_yn', models.BooleanField(db_column='COMPLETE_YN', default=False, verbose_name='완료여부')),
                ('del_yn', models.BooleanField(db_column='DEL_YN', default=False, verbose_name='삭제여부')),
            ],
            options={
                'db_table': 'ESSAY',
            },
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('created_dt', models.DateTimeField(auto_now_add=True, db_column='CREATED_DT', null=True)),
                ('updated_dt', models.DateTimeField(auto_now=True, db_column='UPDATED_DT', null=True)),
                ('keyword_id', models.AutoField(db_column='KEYWORD_ID', primary_key=True, serialize=False, verbose_name='키워드ID')),
                ('keyword_nm', models.CharField(blank=True, db_column='KEYWORD_NM', max_length=16, verbose_name='이름')),
                ('keyword_desc', models.CharField(blank=True, db_column='KEYWORD_DESC', max_length=50, verbose_name='설명')),
            ],
            options={
                'db_table': 'KEYWORD',
            },
        ),
        migrations.CreateModel(
            name='Paragraph',
            fields=[
                ('created_dt', models.DateTimeField(auto_now_add=True, db_column='CREATED_DT', null=True)),
                ('updated_dt', models.DateTimeField(auto_now=True, db_column='UPDATED_DT', null=True)),
                ('paragraph_id', models.AutoField(db_column='PARAGRAPH_ID', primary_key=True, serialize=False, verbose_name='단락ID')),
                ('paragraph_content', models.TextField(blank=True, db_column='PARAGRAPH_CONTENT', verbose_name='내용')),
                ('order', models.IntegerField(db_column='ORDER', default=0, verbose_name='순서')),
                ('del_yn', models.BooleanField(db_column='DEL_YN', default=False, verbose_name='삭제여부')),
                ('essay_id', models.ForeignKey(db_column='ESSAY_ID', on_delete=django.db.models.deletion.PROTECT, related_name='paragraph', to='cowriter.essay', verbose_name='에세이')),
            ],
            options={
                'db_table': 'PARAGRAPH',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('created_dt', models.DateTimeField(auto_now_add=True, db_column='CREATED_DT', null=True)),
                ('updated_dt', models.DateTimeField(auto_now=True, db_column='UPDATED_DT', null=True)),
                ('subject_id', models.CharField(db_column='SUBJECT_ID', max_length=100, primary_key=True, serialize=False, verbose_name='주제ID')),
                ('subject_purpose', models.CharField(db_column='SUBJECT_PURPOSE', max_length=50, verbose_name='목적')),
                ('subject_content', models.TextField(blank=True, db_column='SUBJECT_CONTENT', verbose_name='내용')),
                ('subject_title', models.CharField(db_column='SUBJECT_TITLE', max_length=200, verbose_name='제목')),
                ('del_yn', models.BooleanField(db_column='DEL_YN', default=False, verbose_name='삭제여부')),
            ],
            options={
                'db_table': 'SUBJECT',
            },
        ),
        migrations.CreateModel(
            name='ParagraphHist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_dt', models.DateTimeField(auto_now_add=True, db_column='CREATED_DT', null=True)),
                ('updated_dt', models.DateTimeField(auto_now=True, db_column='UPDATED_DT', null=True)),
                ('change_type', models.CharField(db_column='CHANGE_TYPE', max_length=8, verbose_name='변경타입')),
                ('change_command', models.TextField(blank=True, db_column='CHANGE_COMMAND', verbose_name='변경명령')),
                ('paragraph_content', models.TextField(blank=True, db_column='PARAGRAPH_CONTENT', verbose_name='내용')),
                ('paragraph_id', models.ForeignKey(db_column='PARAGRAPH_ID', on_delete=django.db.models.deletion.PROTECT, related_name='history', to='cowriter.paragraph', verbose_name='단락')),
            ],
            options={
                'db_table': 'PARAGRAPH_HIST',
            },
        ),
        migrations.CreateModel(
            name='EssayMindmap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_dt', models.DateTimeField(auto_now_add=True, db_column='CREATED_DT', null=True)),
                ('updated_dt', models.DateTimeField(auto_now=True, db_column='UPDATED_DT', null=True)),
                ('essay_id', models.ForeignKey(db_column='ESSAY_ID', on_delete=django.db.models.deletion.PROTECT, related_name='mindmap', to='cowriter.essay', verbose_name='에세이')),
                ('keyword1', models.ForeignKey(db_column='KEYWORD_ID', on_delete=django.db.models.deletion.PROTECT, related_name='edge_start', to='cowriter.keyword', verbose_name='키워드1')),
                ('keyword2', models.ForeignKey(db_column='KEYWORD_ID2', on_delete=django.db.models.deletion.PROTECT, related_name='edge_end', to='cowriter.keyword', verbose_name='키워드2')),
            ],
            options={
                'db_table': 'ESSAY_MINDMAP',
            },
        ),
        migrations.AddField(
            model_name='essay',
            name='subject_id',
            field=models.ForeignKey(db_column='SUBJECT_ID', on_delete=django.db.models.deletion.PROTECT, related_name='essay', to='cowriter.subject', verbose_name='주제'),
        ),
    ]
