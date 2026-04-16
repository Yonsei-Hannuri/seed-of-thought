from django.contrib import admin

from ppanzziri.models import (
    BalanceCertification,
    BudgetEffectiveSegment,
    BudgetRecord,
    BudgetRecordTag,
    PushSubscription,
    Social,
    WritingGoal,
)


admin.site.register(BudgetRecord)
admin.site.register(BudgetEffectiveSegment)
admin.site.register(BudgetRecordTag)
admin.site.register(BalanceCertification)
admin.site.register(Social)
admin.site.register(PushSubscription)
admin.site.register(WritingGoal)
