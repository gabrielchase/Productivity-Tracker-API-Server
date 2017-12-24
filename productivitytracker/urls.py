from django.contrib import admin
from django.urls import include, path

from rest_framework_jwt.views import (obtain_jwt_token, refresh_jwt_token, verify_jwt_token)
from rest_framework.routers import DefaultRouter

from users.views import (UserViewSet, LoginAPIView)
from activities.views import ActivityViewSet


router = DefaultRouter()
router.register('users', UserViewSet)
router.register('activities', ActivityViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/login/', LoginAPIView.as_view()),
    path('api/token-auth/', obtain_jwt_token),
    path('api/token-refresh/', refresh_jwt_token),
    path('api/token-verify/', verify_jwt_token),
]
