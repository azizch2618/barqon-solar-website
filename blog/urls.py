from rest_framework.routers import DefaultRouter

from .views import PostViewSet, PostImageViewSet

router = DefaultRouter()
router.register("images", PostImageViewSet, basename="blog-images")
router.register("", PostViewSet, basename="blog")

urlpatterns = router.urls
