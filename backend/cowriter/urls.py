from django.urls import path, include
from rest_framework.routers import DefaultRouter
from cowriter import view


router = DefaultRouter()
router.register(r'subject', view.SubjectViewSet)
router.register(r'keyword', view.KeywordViewSet)
router.register(r'edge', view.EdgeViewSet)
router.register(r'essay', view.EssayViewSet)
router.register(r'topic-sentence', view.TopicSentenceViewSet)
router.register(r'phase', view.PhaseViewSet)


urlpatterns = [path('', include(router.urls)),]