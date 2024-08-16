from django.urls import path, include
from rest_framework.routers import DefaultRouter
from cowriter import view

router = DefaultRouter()
router.register(r'subject', view.SubjectViewSet)
router.register(r'essay', view.EssayViewSet)

essay_router = DefaultRouter()
essay_router.register(r'mindmap', view.EssayMindmapViewSet)
essay_router.register(r'paragraph', view.ParagraphViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('essay/<int:essay_id>/', include(essay_router.urls)),
]