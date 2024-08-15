from django.db import models

class BaseModelMixin(models.Model):
    created_dt = models.DateTimeField(auto_now_add=True, null=True, db_column="CREATED_DT")
    updated_dt = models.DateTimeField(auto_now=True, null=True, db_column="UPDATED_DT")

    class Meta:
        abstract = True
