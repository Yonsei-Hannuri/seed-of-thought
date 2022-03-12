from django.contrib import admin
from hannuri.models import *
import googleDriveAPI
import os
with open('./config/googleDrive/folderId.json') as json_file:
    googleFolderId = json.load(json_file)

class SeasonAdmin(admin.ModelAdmin):
    fields = ('is_current','year', 'semester', 'title', 'leader', 'sessioner', 'socializer')
    
    def save_model(self, request, obj, form, change):
        if obj.is_current==True:
            pre_current_season = Season.objects.all().filter(is_current=True)
            for season in pre_current_season:
                season.is_current = False
                season.save()
        super().save_model(request, obj, form, change)   


class ReadfileInline(admin.TabularInline):
    fields = ('pdf', )
    model = SessionReadfile
    extra = 2
    

class SessionAdmin(admin.ModelAdmin):
    inlines = [ReadfileInline]
    fields = ('is_current', 'week', 'title')

    def save_model(self, request, obj, form, change):
        if obj.is_current==True:
            pre_current_session = Session.objects.all().filter(is_current=True)
            for session in pre_current_session:
                session.is_current = False
                session.save()

            obj.season = Season.objects.get(is_current=True)

        #googleDriveAPI.registerWriter(request.user.email, obj.googleFolderId)

        super().save_model(request, obj, form, change)   

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        files = list(request.FILES.values())
        i=0
        for obj in formset.deleted_objects:
            googleDriveAPI.deletePDF(obj.googleId)
            if os.path.exists('uploads/session/'+obj.googleId+'.pdf'):
                os.remove('uploads/session/'+obj.googleId+'.pdf')
            obj.delete()

        for instance in instances:
            parentFolderId = instance.parentSession.googleFolderId
            PDF = files[i]
            fileName = '읽기자료' + str(instance.parentSession.week) + '주차_' + os.path.splitext(PDF.name)[0] + '.pdf'
            if instance.googleId != '': googleDriveAPI.deletePDF(instance.googleId)
            googleId = googleDriveAPI.savePDF(fileName, parentFolderId, PDF)
            instance.googleId = googleId 
            instance.pdf.name = googleId+'.pdf'
            instance.save()
            i += 1        
        formset.save_m2m()



class UserAdmin(admin.ModelAdmin):
    fields = ('name', 'generation', 'email', 'is_active','is_staff', 'groups')

    def save_model(self, request, obj, form, change):
        if obj.is_active == True and not(obj.permissionId):
            permissionId = googleDriveAPI.registerReader(obj.email, googleFolderId['root'])
            obj.permissionId = permissionId
        elif obj.is_active == False and obj.permissionId:
            googleDriveAPI.deleteMember(obj.permissionId, googleFolderId['root'])
            obj.permissionId = ''

        if obj.is_staff == True and not(obj.writerPermissioned):  
            googleDriveAPI.registerWriter(obj.email, googleFolderId['root'])
            obj.writerPermissioned = True

        elif obj.is_staff == False and obj.writerPermissioned:
            googleDriveAPI.deleteMember(obj.permissionId, googleFolderId['root'])
            permissionId = googleDriveAPI.registerReader(obj.email, googleFolderId['root'])
            obj.permissionId = permissionId
            obj.writerPermissioned = False

        super().save_model(request, obj, form, change)


class FreeNoteAdmin(admin.ModelAdmin):
    fields = ('text', )


admin.site.register(Season, SeasonAdmin)
admin.site.register(Notification)
admin.site.register(User, UserAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(FreeNote, FreeNoteAdmin)