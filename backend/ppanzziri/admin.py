from django.contrib import admin

from ppanzziri.models import (
    BalanceCertification,
    BudgetEffectiveSegment,
    BudgetRecord,
    BudgetRecordTag,
)


admin.site.register(BudgetRecord)
admin.site.register(BudgetEffectiveSegment)
admin.site.register(BudgetRecordTag)
admin.site.register(BalanceCertification)
