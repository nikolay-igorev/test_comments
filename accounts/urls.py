from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("users", UserViewSet)

User = get_user_model()

urlpatterns = router.urls
