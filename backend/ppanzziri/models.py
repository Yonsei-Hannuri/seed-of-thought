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
    photo_url_original = models.TextField(blank=True, default='')
    photo_url_compressed = models.TextField(blank=True, default='')
    photo_url_resized = models.TextField(blank=True, default='')
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


class WritingRecord(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_DONE = 'done'
    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_DONE, 'Done'),
    )

    content = models.TextField()
    char_count = models.PositiveIntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    analysis_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    summary = models.TextField(blank=True, default='')
    keywords = models.JSONField(blank=True, default=list)
    analyzed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'writing_records'
        ordering = ['-submitted_at']


class PushSubscription(models.Model):
    endpoint = models.TextField(unique=True)
    p256dh = models.TextField()
    auth = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'push_subscriptions'
        ordering = ['-created_at']


class WritingGoal(models.Model):
    target_chars = models.PositiveIntegerField(default=1000)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'writing_goal'


