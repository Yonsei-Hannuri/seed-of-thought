from django.urls import path, include
from rest_framework.routers import DefaultRouter
from hannuri import view


router = DefaultRouter()
router.register(r'user', view.UserViewSet)
router.register(r'season', view.SeasonViewSet)
router.register(r'session', view.SessionViewSet)
router.register(r'sessionReadfile', view.SessionReadfileViewSet)
router.register(r'detgori', view.DetgoriViewSet)
router.register(r'detgoriReadTime', view.DetgoriReadTimeViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('login/', view.Login),
    path('signin/', view.Signin),
    path('logout/', view.Logout),
    path('profileColor/', view.ProfileColor),
    path('wordList/<str:type>/<int:sessionId>', view.WordList),
    path('mypageInfo', view.MypageInfo),
    path('frontError/', view.FrontError),
    path('sentenceSearch/', view.SentenceSearch)
]