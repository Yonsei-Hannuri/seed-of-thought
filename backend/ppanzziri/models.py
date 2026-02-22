from django.db import models


class BudgetRecord(models.Model):
    TYPE_EXPENSE = 'EXPENSE'
    TYPE_INCOME = 'INCOME'
    TYPE_CHOICES = (
        (TYPE_EXPENSE, 'Expense'),
        (TYPE_INCOME, 'Income'),
    )

    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    transaction_date = models.DateField()
    amount = models.PositiveBigIntegerField()
    memo = models.TextField(blank=True, default='')
    photo_url = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'budget_records'
        ordering = ['-transaction_date', '-id']


class BudgetEffectiveSegment(models.Model):
    record = models.ForeignKey(BudgetRecord, on_delete=models.CASCADE, related_name='effective_segments')
    effective_from = models.DateField()
    effective_to = models.DateField()
    segment_amount = models.PositiveBigIntegerField()

    class Meta:
        db_table = 'budget_effective_segments'
        ordering = ['effective_from', 'id']


class BudgetRecordTag(models.Model):
    record = models.ForeignKey(BudgetRecord, on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=50)
    amount = models.PositiveBigIntegerField()

    class Meta:
        db_table = 'budget_record_tags'
        ordering = ['-amount', 'name', 'id']


class BalanceCertification(models.Model):
    date = models.DateField(unique=True)
    photo_url = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'balance_certifications'
        ordering = ['-date', '-id']


class Social(models.Model):
    youtube_embed_url = models.TextField(blank=True, default='')
    instagram_post_url = models.TextField(blank=True, default='')
    instagram_profile_url = models.TextField(blank=True, default='')
    extra_links = models.JSONField(blank=True, default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'social'
