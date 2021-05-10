from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'deals/', DealsView, basename='deals')

urlpatterns = router.urls
