from rest_framework.routers import DefaultRouter

from .api_views import AdoptionRequestViewSet, FavoriteViewSet, PetViewSet

router = DefaultRouter()
router.register("pets", PetViewSet, basename="api-pet")
router.register("adoptions", AdoptionRequestViewSet, basename="api-adoption")
router.register("favorites", FavoriteViewSet, basename="api-favorite")

urlpatterns = router.urls
