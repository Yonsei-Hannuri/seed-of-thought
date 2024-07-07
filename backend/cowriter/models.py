from django.db import models

class Subject(models.Model):
    source = models.CharField(max_length=200, verbose_name="출처")
    purpose = models.CharField(max_length=200, verbose_name="목적")
    content = models.TextField(blank=True)

class Keyword(models.Model):
    name = models.CharField(max_length=200, blank=True, verbose_name="이름")
    description = models.CharField(max_length=200, blank=True, verbose_name="이름")

class SubjectKeyword(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, related_name="keyword", verbose_name="주제")
    keyword = models.ForeignKey(Keyword, on_delete=models.PROTECT, related_name="subject", verbose_name="키워드")

class Edge(models.Model):
    owner = models.CharField(max_length=16, verbose_name="사용자")
    # 문자열 순서 상 작은 쪽인 keyword1, 큰 쪽이 keyword2에 들어간다.
    keyword1 = models.ForeignKey(Keyword, on_delete=models.PROTECT, related_name="edge_start", verbose_name="키워드1")
    keyword2 = models.ForeignKey(Keyword, on_delete=models.PROTECT, related_name="edge_end", verbose_name="키워드2")

class Essay(models.Model):
    owner = models.CharField(max_length=16, verbose_name="사용자")
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, related_name="에세이", verbose_name="주제")

class TopicSentence(models.Model):
    essay = models.ForeignKey(Essay, on_delete=models.PROTECT, related_name="topic_sentence", verbose_name="에세이")
    content = models.CharField(max_length=300, blank=True, verbose_name="내용")
    order =  models.IntegerField(default=20, blank=True, verbose_name='순서')

class TopciSentenceKeyword(models.Model):
    topic_senctence = models.ForeignKey(TopicSentence, on_delete=models.PROTECT, related_name="keyword", verbose_name="중심 문장")
    keyword = models.ForeignKey(Keyword, on_delete=models.PROTECT, related_name="topic_sentence", verbose_name="키워드")

class Phase(models.Model):
    topic_sentence = models.ForeignKey(TopicSentence, on_delete=models.PROTECT, related_name="phase", verbose_name="중심 문장")
    content = models.TextField(blank=True)
    is_selected =  models.BooleanField(default=True, verbose_name="선택")
