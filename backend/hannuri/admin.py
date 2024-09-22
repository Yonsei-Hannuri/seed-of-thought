from django.contrib import admin
from hannuri.models import *
from lib import utils
import json
from collections import defaultdict
import os
import uuid
from hannuri.component import objectStorage

class SeasonAdmin(admin.ModelAdmin):
    fields = ('is_current','year', 'semester', 'title', 'leader', 'sessioner', 'socializer')
    
    def save_model(self, request, obj, form, change):
        if obj.is_current==True:

            pre_current_season = Season.objects.all().filter(is_current=True)
            if pre_current_season and len(pre_current_season) == 1 and pre_current_season[0].pk != obj.pk:
                season = pre_current_season[0]
                season_sessions = season.session.all()
                season_detgoris = Detgori.objects.all().filter(parentSession__in=season_sessions)

                season_total_count = defaultdict(int)
                for detgori in season_detgoris:
                    detgori_words = json.loads(detgori.words)
                    for key, value in detgori_words.items():
                        season_total_count[key] += int(value)

                season_total_count_filtered = \
                    utils.filter_dict(season_total_count, lambda x: x[1] > 30)
                season.words = json.dumps(season_total_count_filtered)
                season.is_current = False
                season.save()
    
        super().save_model(request, obj, form, change)   


class ReadfileInline(admin.TabularInline):
    fields = ('googleId', 'pdf')
    readonly_fields = ('googleId',)
    model = SessionReadfile
    extra = 2

    def has_change_permission(self, request, object):
      return False

class SessionAdmin(admin.ModelAdmin):
    inlines = [ReadfileInline]
    fields = ('is_current', 'week', 'title')

    def save_model(self, request, obj, form, change):
        if obj.is_current==True:
            pre_current_session = Session.objects.all().filter(is_current=True)
            for session in pre_current_session:
                session.is_current = False
                session.save()
    
        if not obj.season:
            obj.season = Season.objects.get(is_current=True)

        super().save_model(request, obj, form, change)   

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        files = list(request.FILES.values())

        for obj in formset.deleted_objects:
            obj.delete()
        
        for i, instance in enumerate(instances):
            PDF = files[i]
            session = instance.parentSession
            season = session.season
            short_uuid = str(uuid.uuid4()).split("-")[0]
            fileName = f'{season.year}/{season.semester}학기/{session.week}주차/세션/{os.path.splitext(PDF.name)[0]}-{short_uuid}.pdf'
            objectStorage.save(PDF, fileName, 'application/pdf')
            instance.googleId = fileName
            instance.pdf = None
            instance.save()

        formset.save_m2m()



class UserAdmin(admin.ModelAdmin):
    fields = ('name', 'generation', 'email', 'is_active','is_staff', 'groups')



admin.site.register(Season, SeasonAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Session, SessionAdmin)
