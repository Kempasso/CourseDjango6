from django.urls import include, path
from djoser.views import UserViewSet
from rest_framework.routers import SimpleRouter

# TODO подключите UserViewSet из Djoser.views к нашим urls.py
# TODO для этокого рекоммендуется использовать SimpleRouter
users_router = SimpleRouter()
users_router.register("users", UserViewSet, basename="users")

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("", include(users_router.urls)),
    path('token/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),

]
