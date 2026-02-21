from django.urls import path

from ppanzziri import views


urlpatterns = [
    path('dashboard', views.dashboard),
    path('budget/records', views.budget_records),
    path('budget/records/<int:record_id>', views.budget_record_detail),
    path('budget/tags', views.budget_tags),
    path('budget/certifications', views.budget_certifications),
    path('budget/certifications/<str:certification_date>', views.budget_certification_detail),
]
