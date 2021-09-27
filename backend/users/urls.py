from . import views
from services.views import CustomAuthTokenView

from django.urls import path

from rest_framework import routers


urlpatterns = [
    path(
        'auth/token/login/',
        CustomAuthTokenView.as_view(),
        name='custom_login_view'
    ),
    path(
        'auth/token/logout/',
        CustomAuthTokenView.as_view(),
        name='custom_logout_view'
    ),
    path(
        'users/me/',
        views.UserDetailView.as_view(),
        name='users_detail_view'
    ),
    path(
        'users/set_password/',
        views.UserPasswordView.as_view(),
        name='users_set_password_view'
    ),
    path(
        'users/subscriptions/',
        views.UserSubscriptionView.as_view({'get': 'list'}),
        name='users_subscription_view'
    ),
    path(
        'users/<int:id>/subscribe/',
        views.UserSubscriptionView.as_view(
            {'get': 'create', 'delete': 'destroy'}
        ),
        name='users_subscribe_action_view'
    ),
]

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)

urlpatterns += router.urls
