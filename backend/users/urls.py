from . import views

from django.urls import path

from rest_framework import routers

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path(
        'auth/token/login/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'auth/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'users/me/',
        views.UserDetailView.as_view(),
        name='users_me'
    ),
    path(
        'users/set_password/',
        views.UserPasswordView.as_view(),
        name='users_set_password'
    )
]

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)

urlpatterns += router.urls
