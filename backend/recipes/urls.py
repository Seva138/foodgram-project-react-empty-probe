from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register('recipes', views.RecipeViewSet)
urlpatterns = router.urls
