from django.urls import include, path

# TODO настройка роутов для модели
from rest_framework.routers import SimpleRouter

from ads.views import AdViewSet, AdMeAPIView, CommentViewSet

ads_router = SimpleRouter()
ads_router.register("", AdViewSet, basename='ad')

me_router = SimpleRouter()
me_router.register('', AdMeAPIView, basename='me')

com_router = SimpleRouter()
com_router.register(r"", CommentViewSet, basename='comment')

urlpatterns = [

    path('me/', include(me_router.urls)),
    path('<int:ad_pk>/comments/', include(com_router.urls)),
    path('', include(ads_router.urls)),
]
