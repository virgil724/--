from rest_framework import routers
from .views import ShowViewSet

router = routers.DefaultRouter()
router.register("show", ShowViewSet, basename="show-general")

