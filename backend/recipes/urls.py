from . import views

from django.urls import path

from rest_framework import routers


urlpatterns = [
    path(
        'recipes/<int:id>/favorite/',
        views.UserFavoriteRecipeViewSet.as_view(
            {'get': 'create', 'delete': 'destroy'}
        ),
        name='user_favorite_recipe_view'
    ),
    path(
        'recipes/<int:id>/shopping_cart/',
        views.UserShoppingCartViewSet.as_view(
            {'get': 'create', 'delete': 'destroy'}
        ),
        name='user_shopping_cart_view'
    ),
    path(
        'recipes/download_shopping_cart/',
        views.DownloadShoppingCartView.as_view(),
        name='download_shopping_cart'
    )
]


router = routers.DefaultRouter()

router.register('recipes', views.RecipeViewSet, basename='recipes')
router.register('tags', views.TagViewSet, basename='tags')
router.register('ingredients', views.IngredientViewSet, basename='ingredients')

urlpatterns += router.urls
