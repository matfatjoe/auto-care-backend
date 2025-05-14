from rest_framework.routers import DefaultRouter
from clients.views import ClientViewSet

router = DefaultRouter()
router.register(r"", ClientViewSet, basename="client")

urlpatterns = router.urls
