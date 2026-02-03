from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet
from .views import ServiceMediaViewSet
from .views import ServiceAvailabilityViewSet
from .views import DiscountViewSet

router = DefaultRouter()
router.register('', ServiceViewSet, basename='service')
router.register('media', ServiceMediaViewSet, basename='servicemedia')
router.register('availability', ServiceAvailabilityViewSet, basename='serviceavailability')
router.register('discounts', DiscountViewSet, basename='discount')


urlpatterns = router.urls
