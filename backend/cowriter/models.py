from django.db import models
from common.models.BaseModelMixin import BaseModelMixin

class Subject(BaseModelMixin):
    subject_id = models.CharField(max_length=100, verbose_name="주제ID", primary_key=True, db_column="SUBJECT_ID")
    subject_purpose = models.CharField(max_length=50, verbose_name="목적", db_column="SUBJECT_PURPOSE")
    subject_content = models.TextField(blank=True, verbose_name="내용", db_column="SUBJECT_CONTENT")
    del_yn = models.BooleanField(default=False, verbose_name="삭제여부", db_column="DEL_YN")

    class Meta:
        db_table = "SUBJECT"

class Keyword(BaseModelMixin):
    keyword_id = models.AutoField(primary_key=True, verbose_name="키워드ID", db_column="KEYWORD_ID")
    keyword_nm = models.CharField(max_length=16, blank=True, verbose_name="이름", db_column="KEYWORD_NM")
    keyword_desc = models.CharField(max_length=50, blank=True, verbose_name="설명", db_column="KEYWORD_DESC")

    class Meta:
        db_table = "KEYWORD"

class Essay(BaseModelMixin):
    essay_id = models.AutoField(primary_key=True, verbose_name="에세이ID", db_column="ESSAY_ID")
    subject_id = models.ForeignKey(Subject, on_delete=models.PROTECT, related_name="essay", verbose_name="주제", db_column="SUBJECT_ID")
    owner = models.CharField(max_length=100, verbose_name="사용자", db_column="OWNER_ID")
    complete_yn = models.BooleanField(default=False, verbose_name="완료여부", db_column="COMPLETE_YN")
    del_yn = models.BooleanField(default=False, verbose_name="삭제여부", db_column="DEL_YN")

    class Meta:
        db_table = "ESSAY"

class EssayMindmap(BaseModelMixin):
    essay_id = models.ForeignKey(Essay, on_delete=models.PROTECT, related_name="mindmap", verbose_name="에세이", db_column="ESSAY_ID")
    # 문자열 순서 상 작은 쪽인 keyword1, 큰 쪽이 keyword2에 들어간다.
    keyword1 = models.ForeignKey(Keyword, on_delete=models.PROTECT, related_name="edge_start", verbose_name="키워드1", db_column="KEYWORD_ID")
    keyword2 = models.ForeignKey(Keyword, on_delete=models.PROTECT, related_name="edge_end", verbose_name="키워드2", db_column="KEYWORD_ID2")

    class Meta:
        db_table = "ESSAY_MINDMAP"

class Paragraph(BaseModelMixin):
    paragraph_id = models.AutoField(primary_key=True, verbose_name="단락ID", db_column="PARAGRAPH_ID")
    essay_id = models.ForeignKey(Essay, on_delete=models.PROTECT, related_name="paragraph", verbose_name="에세이", db_column="ESSAY_ID")
    paragraph_content = models.TextField(blank=True, verbose_name="내용", db_column="PARAGRAPH_CONTENT")
    order = models.IntegerField(default=0, verbose_name="순서", db_column="ORDER")
    del_yn = models.BooleanField(default=False, verbose_name="삭제여부", db_column="DEL_YN")

    class Meta:
        db_table = "PARAGRAPH"

class ParagraphHist(BaseModelMixin):
    paragraph_id = models.ForeignKey(Paragraph, on_delete=models.PROTECT, related_name="history", verbose_name="단락", db_column="PARAGRAPH_ID")
    change_type = models.CharField(max_length=8, verbose_name="변경타입", db_column="CHANGE_TYPE")
    change_command = models.TextField(blank=True, verbose_name="변경명령", db_column="CHANGE_COMMAND")
    paragraph_content = models.TextField(blank=True, verbose_name="내용", db_column="PARAGRAPH_CONTENT")

    class Meta:
        db_table = "PARAGRAPH_HIST"