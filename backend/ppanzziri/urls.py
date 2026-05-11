from django.urls import path

from ppanzziri import views


urlpatterns = [
    path('dashboard', views.dashboard),
    path('social', views.social),
    path('budget/records', views.budget_records),
    path('budget/records/<int:record_id>', views.budget_record_detail),
    path('budget/tags', views.budget_tags),
    path('writing/records', views.writing_records),
    path('writing/records/<int:record_id>', views.writing_record_detail),
    path('writing/dashboard', views.writing_dashboard),
]
