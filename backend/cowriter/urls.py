from django.urls import path, include
from rest_framework.routers import DefaultRouter
from cowriter import view


router = DefaultRouter()
router.register(r'subject', view.SubjectViewSet)
router.register(r'keyword', view.KeywordViewSet)
router.register(r'essay', view.EssayViewSet)
router.register(r'mindmap', view.EssayMindmapViewSet)
router.register(r'phase', view.PhaseViewSet)


urlpatterns = [path('', include(router.urls)),]