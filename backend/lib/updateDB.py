from hannuri.models import *

def updateAll(table, logic):
    rows = table.objects.all()
    for row in rows:
        logic(row)

def actingSeasonChange(user):
    act_seasons = list(map(int, user.actingSeason.split()))
    for season in act_seasons:
        user.act_seasons.add(season)
    user.save()

if __name__ == "django.core.management.commands.shell":
    updateAll(User, actingSeasonChange)